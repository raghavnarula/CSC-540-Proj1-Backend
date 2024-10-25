from sqlmodel import Field, SQLModel, Relationship # type: ignore
from typing import Optional


class Course(SQLModel, table=True):
    course_id: str = Field(index=True, unique=True, primary_key=True)
    course_name: str
    etextbook_id: str
    course_type: str
    
    # Foreign keys referencing the User table
    faculty_member_id: str
    ta_id: str

    start_date: str  
    end_date: str
    unique_token: str
    course_capacity: int