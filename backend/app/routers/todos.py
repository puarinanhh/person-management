from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut

router = APIRouter()


def current_user_id() -> int:
    return 1


@router.get("/", response_model=list[TodoOut])
def list_todos(db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    return db.query(Todo).filter(Todo.user_id == user_id).order_by(Todo.id.desc()).all()


@router.post("/", response_model=TodoOut)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    item = Todo(user_id=user_id, title=payload.title, done=payload.done)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    item = db.get(Todo, todo_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Todo not found")
    if payload.title is not None:
        item.title = payload.title
    if payload.done is not None:
        item.done = payload.done
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), user_id: int = Depends(current_user_id)):
    item = db.get(Todo, todo_id)
    if not item or item.user_id != user_id:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(item)
    db.commit()
    return {"ok": True}
