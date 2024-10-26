from sqlmodel import Field, SQLModel, Relationship # type: ignore
from typing import Optional

class Textbook(SQLModel, table=True):
    textbook_id: str = Field(index=True, unique=True, primary_key=True)
    title: str