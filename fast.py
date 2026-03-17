from fastapi import FastAPI, HTTPException
import json
import os
from struct12 import Task 
from dataclasses import dataclass
from pydantic import BaseModel
from struct12 import Task

app = FastAPI()
TASK_FILE = "tasks.json"
ID_FILE = "next_id.json"

# Pydantic models
class TaskIn(BaseModel):
    title: str
    completed: bool = False

class TaskUpdate(BaseModel):
    completed: bool

# Load tasks safely
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, "r") as file:
            data = json.load(file)
            tasks = []
            for item in data:
                task = Task(item["id"], item["title"])
                task.completed = item.get("completed", False)
                tasks.append(task)
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks
def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump([t.to_dict() for t in tasks], file, indent=4)

# Load next ID
def load_next_id():
    if not os.path.exists(ID_FILE):
        return 1
    try:
        with open(ID_FILE, "r") as file:
            data = json.load(file)
            return data.get("next_id", 1)
    except (FileNotFoundError, json.JSONDecodeError):
        return 1

# Save next ID
def save_next_id(next_id):
    with open(ID_FILE, "w") as file:
        json.dump({"next_id": next_id}, file, indent=4)

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API!"}

# Get all tasks
@app.get("/tasks")
def get_tasks():
    tasks = load_tasks()
    return {"tasks": [t.to_dict() for t in tasks]}

# Add a new task
@app.post("/tasks")
def add_task(task: TaskIn):
    tasks = load_tasks()
    next_id = load_next_id()

    new_task = Task(next_id, task.title)
    new_task.completed = task.completed
    tasks.append(new_task)
    save_tasks(tasks)

    next_id += 1
    save_next_id(next_id)

    return {"message": "Task added successfully", "task": new_task.to_dict()}

# Update task completion
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed = task_update.completed
            save_tasks(tasks)
            return {"message": "Task updated", "task": task.to_dict()}

    raise HTTPException(status_code=404, detail="Task not found")

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task.id == task_id:
            removed_task = tasks.pop(i)
            save_tasks(tasks)
            return {"message": "Task deleted", "task": removed_task.to_dict()}

    raise HTTPException(status_code=404, detail="Task not found")
