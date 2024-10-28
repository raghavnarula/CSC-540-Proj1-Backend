from fastapi import APIRouter, Depends, HTTPException,Query,Request #type:ignore
from sqlmodel import Session, select, SQLModel, Field # type: ignore
from ..database import get_session
from ..models import users
from datetime import datetime

router = APIRouter()

@router.post("/users/",response_model=users.User,tags=['users'])
def create_user(user: users.User,  role:str = Query("admin"),session: Session = Depends(get_session)):
    # Check if username already exists
    existing_user = session.exec(select(users.User).where(users.User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    # Generate user ID based on FirstName, LastName, and creation date
    current_date = datetime.utcnow()
    user_id = f"{user.FirstName[:2].upper()}{user.LastName[:2].upper()}{current_date.strftime('%m%Y')}"
    
    # Assign the generated ID and the creation date to the user
    user.id = user_id
    user.CreationDate = current_date
    user.role = role
    
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

