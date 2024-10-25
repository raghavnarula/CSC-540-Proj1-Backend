from sqlmodel import Field, SQLModel, Relationship # type: ignore
from typing import Optional


class Chapter(SQLModel, table=True):
    textbook_id: str
    Chapter_id:str = Field(index=True, unique=True, primary_key=True)
    title: str
    hidden: bool