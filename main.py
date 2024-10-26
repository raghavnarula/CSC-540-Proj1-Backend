from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .routers import users,courses,login,textbooks
from typing import Annotated
from .database import *

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include the users router
app.include_router(login.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(textbooks.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}
