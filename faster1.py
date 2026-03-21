from typing import Optional

from fastapi import FastAPI, HTTPException,Depends
from dataclasses import dataclass
from pydantic import BaseModel
from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import Session, declarative_base,sessionmaker

engine=create_engine("postgresql://postgres:0@localhost:5432/todo_db")
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

class Task(Base):
    __tablename__="tasks"

    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    completed=Column(Boolean,default=False)

Base.metadata.create_all(engine)
app = FastAPI()

# Pydantic models
class TaskIn(BaseModel):
    title: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks")
def add_task(task: TaskIn, db:Session = Depends(get_db)):

    new_task = Task(title=task.title)
    new_task.completed = task.completed
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added successfully", "task": {"id": new_task.id, "title": new_task.title, "completed": new_task.completed}}


@app.get("/tasks")
def get_tasks(completed : Optional[bool],db: Session =Depends(get_db)):
    query=db.query()
    if completed is not None:
        query=query.filter(Task.completed==completed)

    tasks=query.all()
    return tasks

@app.put("/tasks/{task_id}",response_model=TaskResponse)
def update_task(task_id: int, task: TaskIn, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task=db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": f"{task_id} deleted successfully"}