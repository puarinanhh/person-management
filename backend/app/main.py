from fastapi import FastAPI
from app.routers import notes, todos
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.models import user as _user_model
from app.models import note as _note_model
from app.models import todo as _todo_model  

app = FastAPI(title="Personal Dashboard API")
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(todos.router, prefix="/todos", tags=["todos"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health(): return {"status": "ok"}
