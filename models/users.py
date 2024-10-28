from sqlmodel import Field, SQLModel, Relationship # type:ignore
from typing import Optional, List
from enum import Enum
from .courses import Course
from datetime import datetime

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
    FirstName: str
    LastName: str
    email_id: str
    CreationDate: datetime = Field(default_factory=datetime.utcnow)
    enrollments: List["Enrollment"] = Relationship(back_populates="student")