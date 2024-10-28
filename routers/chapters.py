from fastapi import APIRouter, Depends, HTTPException, Request, status #type:ignore
from sqlmodel import Session, select #type:ignore
from ..database import get_session
from ..models.textbook import chapter  # Assuming chapter is the module with the chapter model

router = APIRouter()

@router.post("/chapter/", response_model=chapter.chapter, tags=['chapter'], status_code=status.HTTP_200_OK)
def create_chapter(request:Request, chapter: chapter.chapter, session: Session = Depends(get_session)):
    # Optionally use a cookie for authorization or logging purposes
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to create chapter"
        )
    else:
        # Check if the chapter already exists
        existing_chapter = session.exec(select(chapter.chapter).where(chapter.chapter.chapter_id == chapter.chapter_id)).first()
        if existing_chapter:
            raise HTTPException(status_code=400, detail="chapter with this ID already exists")
        session.add(chapter)
        session.commit()
        session.refresh(chapter)
        return chapter

@router.get("/chapter/{chapter_id}", response_model=chapter.chapter, tags=['chapter'])
def read_chapter(request:Request, chapter_id: str, session: Session = Depends(get_session)):
    chapter = session.get(chapter.chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="chapter not found")
    return chapter

@router.get("/chapter/", response_model=list[chapter.chapter], tags=["chapter"])
def read_chapter(request:Request, session: Session = Depends(get_session)):
    try:
        chapter_list = session.exec(select(chapter.chapter)).all()
        return chapter_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/chapter/{chapter_id}", response_model=chapter.chapter, tags=["chapter"])
def update_chapter(request:Request,chapter_id: str, updated_chapter: chapter.chapter, session: Session = Depends(get_session)):
    user_role = request.cookies.get("user_role")
    if not user_role or user_role != "UserRole.admin":
        raise HTTPException(
            status_code=400, 
            detail="You are not allowed to update chapter"
        )
    else:
        db_chapter = session.get(chapter.chapter, chapter_id)
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
        db_chapter = session.get(chapter.chapter, chapter_id)
        if not db_chapter:
            raise HTTPException(status_code=404, detail="chapter not found")
        
        session.delete(db_chapter)
        session.commit()
        return {"message": "chapter deleted successfully"}
