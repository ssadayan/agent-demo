from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import engine, get_db, Base
from models import User, Todo
from schemas import UserRegister, UserLogin, TodoCreate, TodoUpdate
from auth import create_access_token, get_current_user, hash_password, verify_password

load_dotenv()

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Auth routes
@app.post("/api/auth/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = hash_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id)})
    return {"token": token, "user": {"id": str(new_user.id), "email": new_user.email}}


@app.post("/api/auth/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(db_user.id)})
    return {"token": token, "user": {"id": str(db_user.id), "email": db_user.email}}


# Todo routes
@app.get("/api/todos")
def get_todos(user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    todos = db.query(Todo).filter(Todo.user_id == user_id).all()
    return todos


@app.post("/api/todos", status_code=201)
def create_todo(todo: TodoCreate, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title, priority=todo.priority, due_date=todo.due_date, user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: str, todo: TodoUpdate, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = todo.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}


@app.patch("/api/todos/{todo_id}/done")
def toggle_todo(todo_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.status = "done" if db_todo.status != "done" else "pending"
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
