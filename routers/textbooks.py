from fastapi import APIRouter, Depends, HTTPException, Request, status #type:ignore
from sqlmodel import Session, select #type:ignore
from ..database import get_session
from ..models.textbook import textbooks  # Assuming textbooks is the module with the Textbook model

router = APIRouter()

@router.post("/textbooks/", response_model=textbooks.Textbook, tags=['textbooks'], status_code=status.HTTP_200_OK)
def create_textbook(request:Request, textbook: textbooks.Textbook, session: Session = Depends(get_session)):
    # Optionally use a cookie for authorization or logging purposes
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to create textbooks"
        )
    else:
        # Check if the textbook already exists
        existing_textbook = session.exec(select(textbooks.Textbook).where(textbooks.Textbook.textbook_id == textbook.textbook_id)).first()
        if existing_textbook:
            raise HTTPException(status_code=400, detail="Textbook with this ID already exists")
        session.add(textbook)
        session.commit()
        session.refresh(textbook)
        return textbook

@router.get("/textbooks/{textbook_id}", response_model=textbooks.Textbook, tags=['textbooks'])
def read_textbook(request:Request, textbook_id: str, session: Session = Depends(get_session)):
    textbook = session.get(textbooks.Textbook, textbook_id)
    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook not found")
    return textbook

@router.get("/textbooks/", response_model=list[textbooks.Textbook], tags=["textbooks"])
def read_textbooks(request:Request, session: Session = Depends(get_session)):
    try:
        textbook_list = session.exec(select(textbooks.Textbook)).all()
        return textbook_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/textbooks/{textbook_id}", response_model=textbooks.Textbook, tags=["textbooks"])
def update_textbook(request:Request,textbook_id: str, updated_textbook: textbooks.Textbook, session: Session = Depends(get_session)):
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to update textbooks"
        )
    else:
        db_textbook = session.get(textbooks.Textbook, textbook_id)
        if not db_textbook:
            raise HTTPException(status_code=404, detail="Textbook not found")
        
        db_textbook.title = updated_textbook.title
        session.add(db_textbook)
        session.commit()
        session.refresh(db_textbook)
        return db_textbook

@router.delete("/textbooks/{textbook_id}", tags=["textbooks"])
def delete_textbook(request:Request, textbook_id: str, session: Session = Depends(get_session)):
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to delete textbooks"
        )
    else:
        db_textbook = session.get(textbooks.Textbook, textbook_id)
        if not db_textbook:
            raise HTTPException(status_code=404, detail="Textbook not found")
        
        session.delete(db_textbook)
        session.commit()
        return {"message": "Textbook deleted successfully"}
