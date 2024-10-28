from sqlmodel import Field, SQLModel, Relationship # type: ignore
from typing import Optional


class Chapter(SQLModel, table=True):
    textbook_id: str
    Chapter_id:str = Field(index=True, unique=True, primary_key=True)
    title: str
    hidden: bool

class Sections(SQLModel, table=True):
    section_id: str = Field(index=True, unique=True, primary_key=True)
    textbook_id: str
    chapter_id:str
    title: str
    hidden: bool

class Textbook(SQLModel, table=True):
    textbook_id: str = Field(index=True, unique=True, primary_key=True)
    title: str

class Activities(SQLModel,table=True):
    id: str = Field(index=True,primary_key=True)
    pass

class Questions(SQLModel,table=True):
    id: str = Field(index=True,primary_key=True)
    pass

class Blocks(SQLModel,table=True):
    id: str = Field(index=True,primary_key=True)
    pass
