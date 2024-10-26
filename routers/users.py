from fastapi import APIRouter, Depends, HTTPException, Request #type:ignore
from sqlmodel import Session, select, SQLModel, Field # type: ignore
from ..database import get_session
from ..models import users

router = APIRouter()

@router.post("/users/", response_model=users.User,tags=['users'])
def create_user(user: users.User, session: Session = Depends(get_session)):
    # Check if username already exists
    existing_user = session.exec(select(users.User).where(users.User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/{user_id}", response_model=users.User,tags=['users'])
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(users.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/", response_model=list[users.User], tags=["users"])
def read_users(session: Session = Depends(get_session)):
    try:
        user_list = session.exec(select(users.User)).all()
        return user_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

