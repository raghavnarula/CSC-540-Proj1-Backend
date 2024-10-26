from fastapi import APIRouter, Depends, HTTPException,Cookie #type:ignore
from sqlmodel import Session, select, SQLModel, Field # type: ignore
from ..database import get_session
from ..models import courses, users, enrollment

router = APIRouter()

# add a new course
@router.post("/courses/", response_model=courses.Course, tags=["courses"])
def create_course(course: courses.Course, session: Session = Depends(get_session), user_role: str = Cookie(None)):
    # Check if the user_role is provided and is either 'faculty' or 'admin'
    if user_role not in ['UserRole.admin','UserRole.faculty']:
        raise HTTPException(status_code=403, detail="Not allowed to create a course")

    # Check if course_id already exists
    existing_course = session.exec(select(courses.Course).where(courses.Course.course_id == course.course_id)).first()
    if existing_course:
        raise HTTPException(status_code=400, detail="Course ID already exists")

    session.add(course)
    session.commit()
    session.refresh(course)
    return course

# get particular coourse information
@router.get("/courses/{course_id}", response_model=courses.Course, tags=["courses"])
def read_course(course_id: str, session: Session = Depends(get_session)):
    course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# get all courses
@router.get("/courses/", response_model=list[courses.Course], tags=["courses"])
def read_courses(session: Session = Depends(get_session)):
    return session.exec(select(courses.Course)).all()

# update the courses
@router.put("/courses/{course_id}", response_model=courses.Course, tags=["courses"])
def update_course(course_id: str, course: courses.Course, session: Session = Depends(get_session)):
    db_course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.course_name = course.course_name
    db_course.etextbook_id = course.etextbook_id
    db_course.course_type = course.course_type
    db_course.faculty_member_id = course.faculty_member_id
    db_course.ta_id = course.ta_id
    db_course.start_date = course.start_date
    db_course.end_date = course.end_date
    db_course.unique_token = course.unique_token
    db_course.course_capacity = course.course_capacity
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

# delete a course
@router.delete("/courses/{course_id}", response_model=dict, tags=["courses"])
def delete_course(course_id: str, session: Session = Depends(get_session)):
    course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    session.delete(course)
    session.commit()
    return {"message": "Course deleted successfully"}

# view worklist
@router.get("/courses/{course_id}/worklist", response_model=list, tags=["courses"])
def view_worklist(course_id: str, session: Session = Depends(get_session)):
    # Fetch the course based on course_id
    course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Query to get students with pending enrollment status in the course
    worklist = session.exec(
        select(enrollment.Enrollment).where(
            enrollment.Enrollment.course_id == course_id,
            enrollment.Enrollment.status == enrollment.EnrollmentStatus.pending
        )
    ).all()

    # Collect student information from the pending enrollments
    student_ids = [enrollment.student_id for enrollment in worklist]
    students = session.exec(select(users.User).where(users.User.id.in_(student_ids))).all()

    if not students:
        raise HTTPException(status_code=404, detail="No students pending approval for this course")

    return [{"student_id": student.id, "username": student.username} for student in students]

# approve enrollment
@router.post("/courses/{course_id}/approve-enrollment", response_model=dict, tags=["courses"])
def approve_enrollment(course_id: str, student_id: str, approve: bool, session: Session = Depends(get_session)):
    # Fetch the course based on the course_id
    course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Fetch the enrollment record based on student_id and course_id
    enrollment_record = session.exec(
        select(enrollment.Enrollment).where(
            enrollment.Enrollment.student_id == student_id,
            enrollment.Enrollment.course_id == course_id
        )
    ).first()

    if not enrollment_record:
        raise HTTPException(status_code=404, detail="Enrollment record not found")

    # Update approval status based on the approve parameter
    enrollment_record.status = enrollment.EnrollmentStatus.enrolled if approve else enrollment.EnrollmentStatus.rejected
    session.add(enrollment_record)
    session.commit()
    session.refresh(enrollment_record)

    status_message = "approved" if approve else "rejected"
    return {"message": f"Student enrollment has been {status_message}", "student_id": student_id, "status": enrollment_record.status}

# view students
@router.get("/courses/{course_id}/students", response_model=list, tags=["courses"])
def view_students(course_id: str, session: Session = Depends(get_session)):
    # Fetch the course based on course_id
    course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Fetch all enrollments with "Enrolled" status for the course
    enrolled_students = session.exec(
        select(enrollment.Enrollment).where(
            enrollment.Enrollment.course_id == course_id,
            enrollment.Enrollment.status == enrollment.EnrollmentStatus.enrolled
        )
    ).all()

    if not enrolled_students:
        raise HTTPException(status_code=404, detail="No enrolled students found for this course")

    # Collect student information from the enrollments
    student_ids = [enrollment.student_id for enrollment in enrolled_students]
    students = session.exec(select(users.User).where(users.User.id.in_(student_ids))).all()

    return [{"student_id": student.id, "username": student.username} for student in students]

# add student enrollment
@router.post("/courses/{course_id}/enroll", response_model=dict, tags=["courses"])
def add_enrollment(course_id: str, student_id: str, session: Session = Depends(get_session)):
    # Fetch the course based on course_id
    course = session.exec(select(courses.Course).where(courses.Course.course_id == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Fetch the student based on student_id
    student = session.exec(select(users.User).where(users.User.id == student_id)).first()
    if not student or student.role != "student":
        raise HTTPException(status_code=404, detail="Student not found")

    # Check if the student is already enrolled in the course
    existing_enrollment = session.exec(
        select(enrollment.Enrollment).where(
            enrollment.Enrollment.course_id == course_id,
            enrollment.Enrollment.student_id == student_id
        )
    ).first()

    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    # Create a new enrollment with status "Pending"
    new_enrollment = enrollment.Enrollment(
        student_id=student_id,
        course_id=course_id,
        status=enrollment.EnrollmentStatus.pending
    )

    session.add(new_enrollment)
    session.commit()
    session.refresh(new_enrollment)

    return {"message": "Enrollment request submitted successfully", "student_id": student_id, "course_id": course_id}