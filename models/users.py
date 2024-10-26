from sqlmodel import Field, SQLModel, Relationship # type:ignore
from typing import Optional, List
from enum import Enum
from .courses import Course

class UserRole(str, Enum):
    admin = "admin"
    faculty = "faculty"
    ta = "ta"
    student = "student"

class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: UserRole

    enrollments: List["Enrollment"] = Relationship(back_populates="student")