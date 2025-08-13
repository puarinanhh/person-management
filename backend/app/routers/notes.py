from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut

router = APIRouter()

# Demo: coi như đã auth, dùng user_id=1

def current_user_id() -> int:
    return 1

@router.get("/", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    return db.query(Note).filter(Note.user_id == user_id).order_by(Note.id.desc()).all()

@router.post("/", response_model=NoteOut)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    note = Note(user_id=user_id, title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    note = db.get(Note, note_id)
    if not note or note.user_id != user_id:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    note = db.get(Note, note_id)
    if not note or note.user_id != user_id:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"ok": True}