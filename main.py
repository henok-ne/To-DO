from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine, Base
from security import hash_password, verify_password
from auth import create_token, decode_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    print("token recieved:",token)
    user_id = decode_token(token)
    
    if not user_id:
        raise HTTPException(401, "Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(401, "User not found")

    return user


@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed = hash_password(user.password)

        db_user = models.User(
            username=user.username,
            hashed_password=hashed
        )

        db.add(db_user)
        db.commit()

        return {"msg": "user created"}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(500, str(e))



from fastapi.security import OAuth2PasswordRequestForm

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    token = create_token(db_user.id)
    return {"access_token": token, "token_type": "bearer"}



@app.post("/tasks", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    t = models.Task(
        title=task.title,
        owner_id=user.id
    )

    db.add(t)
    db.commit()
    db.refresh(t)

    return t


@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(models.Task).filter(
        models.Task.owner_id == user.id
    ).all()

# main.py
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task_put(
    task_id: int,
    task_data: schemas.TaskPut,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_data.title
    task.completed = task_data.completed

    db.commit()
    db.refresh(task)
    return task


# main.py
@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}