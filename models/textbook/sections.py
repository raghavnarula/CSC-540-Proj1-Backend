from sqlmodel import Field, SQLModel, Relationship # type: ignore
from typing import Optional


class Sections(SQLModel, table=True):
    section_id: str = Field(index=True, unique=True, primary_key=True)
    textbook_id: str
    chapter_id:str
    title: str
    hidden: bool