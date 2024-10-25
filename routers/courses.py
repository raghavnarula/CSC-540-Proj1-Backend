from fastapi import APIRouter, Depends, HTTPException,Cookie #type:ignore
from sqlmodel import Session, select, SQLModel, Field # type: ignore
from ..database import get_session
from ..models import courses

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