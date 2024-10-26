from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from enum import Enum

class EnrollmentStatus(str, Enum):
    pending = "Pending"
    enrolled = "Enrolled"

class Enrollment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(foreign_key="user.id")
    course_id: str = Field(foreign_key="course.course_id")
    status: EnrollmentStatus = Field(default=EnrollmentStatus.pending)

    # Relationships
    student: "User" = Relationship(back_populates="enrollments")
    course: "Course" = Relationship(back_populates="enrollments")