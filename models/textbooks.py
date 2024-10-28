from sqlmodel import Field, SQLModel, Relationship # type: ignore
from typing import Optional
from typing import List


from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Chapter(SQLModel, table=True):
    chapter_id: str = Field(index=True, unique=True, primary_key=True)
    textbook_id: str = Field(foreign_key="textbook.textbook_id")  # Foreign key to Textbook
    title: str
    hidden: bool

    # Relationship to link back to Textbook
    textbook: Optional["Textbook"] = Relationship(back_populates="chapters")


class Textbook(SQLModel, table=True):
    textbook_id: str = Field(index=True, unique=True, primary_key=True)
    title: str

    # Relationship to link Textbook to Chapters
    chapters: List[Chapter] = Relationship(back_populates="textbook", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Sections(SQLModel, table=True):
    section_id: str = Field(index=True, unique=True, primary_key=True)
    textbook_id: str
    chapter_id: str
    title: str
    hidden: bool
    

class Activities(SQLModel,table=True):
    id: str = Field(index=True,primary_key=True)
    pass

class Questions(SQLModel,table=True):
    id: str = Field(index=True,primary_key=True)
    pass

class Blocks(SQLModel,table=True):
    id: str = Field(index=True,primary_key=True)
    pass
