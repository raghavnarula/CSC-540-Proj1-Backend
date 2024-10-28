from fastapi import APIRouter, Depends, HTTPException, Request, status #type:ignore
from sqlmodel import Session, select #type:ignore
from ..database import get_session
from ..models import textbooks   # Assuming chapter is the module with the chapter model

router = APIRouter()

@router.post("/chapter/", response_model=textbooks.Chapter, tags=['chapter'], status_code=status.HTTP_200_OK)
def create_chapter(request: Request, chapter_data: textbooks.Chapter, session: Session = Depends(get_session)):
    # Check user role from cookies
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400,
            detail="You are not allowed to create a chapter"
        )
    # Check if the chapter already exists
    existing_chapter = session.exec(select(textbooks.Chapter).where(textbooks.Chapter.chapter_id == chapter_data.chapter_id)).first()
    if existing_chapter:
        raise HTTPException(status_code=400, detail="Chapter with this ID already exists")
    
    existing_textbook = session.exec(select(textbooks.Textbook).where(textbooks.Textbook.textbook_id == chapter_data.textbook_id)).first()
    if not existing_textbook:
        raise HTTPException(status_code=400, detail="Textbook with this ID does not exist")
    
    # Create a new chapter instance and add it to the session
    new_chapter = textbooks.Chapter(**chapter_data.dict())
    session.add(new_chapter)
    session.commit()
    session.refresh(new_chapter)    
    return new_chapter

@router.get("/chapter/{chapter_id}", response_model=textbooks.Chapter, tags=['chapter'])
def read_chapter(request: Request, chapter_id: str, session: Session = Depends(get_session)):
    chapter = session.get(textbooks.Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.get("/chapter/", response_model=list[textbooks.Chapter], tags=["chapter"])
def read_chapter(request:Request, session: Session = Depends(get_session)):
    try:
        chapter_list = session.exec(select(textbooks.Chapter)).all()
        return chapter_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/chapter/{chapter_id}", response_model=textbooks.Chapter, tags=["chapter"])
def update_chapter(request:Request,chapter_id: str, updated_chapter: textbooks.Chapter, session: Session = Depends(get_session)):
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to update chapter"
        )
    else:
        db_chapter = session.get(textbooks.Chapter, chapter_id)
        if not db_chapter:
            raise HTTPException(status_code=404, detail="chapter not found")
        
        db_chapter.title = updated_chapter.title
        session.add(db_chapter)
        session.commit()
        session.refresh(db_chapter)
        return db_chapter

@router.delete("/chapter/{chapter_id}", tags=["chapter"])
def delete_chapter(request:Request, chapter_id: str, session: Session = Depends(get_session)):
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to delete chapter"
        )
    else:
        db_chapter = session.get(textbooks.Chapter, chapter_id)
        if not db_chapter:
            raise HTTPException(status_code=404, detail="chapter not found")
        
        session.delete(db_chapter)
        session.commit()
        return {"message": "chapter deleted successfully"}

