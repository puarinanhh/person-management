from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str | None = None

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class NoteOut(BaseModel):
    id: int
    title: str
    content: str | None
    class Config:
        from_attributes = True