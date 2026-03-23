from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from security import hash_password, verify_password
from auth import create_access_token, decode_access_token


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Pydantic Models
class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None
    completed: bool | None

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current user dependency
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Signup
@app.post("/signup", status_code=201)
def signup(username: str, password: str, db: Session = Depends(get_db)):
    hashed = hash_password(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    return {"message": "user created"}

# Login
@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(user.id)
    return {"access_token": token}

# Create Task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    t = models.Task(title=task.title, completed=False, owner_id=current_user.id)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

# Read Tasks
@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(skip: int = 0, limit: int = 10, completed: bool | None = None, title: str | None = None,
              db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    if title:
        query = query.filter(models.Task.title.contains(title))
    return query.offset(skip).limit(limit).all()

# Update Task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    t = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.title is not None:
        t.title = task.title
    if task.completed is not None:
        t.completed = task.completed
    db.commit()
    db.refresh(t)
    return t

# Delete Task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    t = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if not t:
            raise HTTPException(status_code=404, detail="Task not found")
    db.delete(t)
    db.commit()
    return 