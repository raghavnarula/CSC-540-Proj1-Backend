from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from ..database import get_session
from ..models import users

router = APIRouter()
@router.post("/login",tags=['login'])
def login(username: str, password: str, response: Response, session: Session = Depends(get_session)):
    # Query the database to find a matching username and password
    user = session.exec(
        select(users.User).where(users.User.username == username, users.User.password == password)
    ).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    # Set cookies with the user's role and ID if authentication is successful
    response.set_cookie(key="user_role", value=user.role, httponly=True, samesite="Lax")
    response.set_cookie(key="user_id", value=str(user.id), httponly=True, samesite="Lax")
    
    return {"message": f"Welcome {username}!"}
