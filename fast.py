from fastapi import FastAPI, HTTPException
import json
import os
from struct12 import Task 
from dataclasses import dataclass

app = FastAPI()
TASK_FILE = "tasks.json"
ID_FILE = "next_id.json"  # To track next unique ID

# -------------------- Task Model --------------------
@dataclass
class Task:
    id: int
    title: str
    completed: bool = False

    def toggle(self):
        self.completed = not self.completed

    def to_dict(self):
        return {"id": self.id, "title": self.title, "completed": self.completed}

# -------------------- Helper Functions --------------------
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, "r") as file:
            data = json.load(file)
            tasks = []
            for item in data:
                task = Task(item["id"], item["title"])
                task.completed = item["completed"]
                tasks.append(task)
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)

# -------------------- ID Tracking --------------------
def load_next_id():
    if not os.path.exists(ID_FILE):
        return 1
    try:
        with open(ID_FILE, "r") as file:
            data = json.load(file)
            return data.get("next_id", 1)
    except (FileNotFoundError, json.JSONDecodeError):
        return 1

def save_next_id(next_id):
    with open(ID_FILE, "w") as file:
        json.dump({"next_id": next_id}, file)

# -------------------- API Routes --------------------
@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API!"}

@app.get("/tasks")
def get_tasks():
    tasks = load_tasks()
    return {"tasks": [task.to_dict() for task in tasks]}

@app.post("/tasks")
def add_task(title: str):
    tasks = load_tasks()
    next_id = load_next_id()

    if not title.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty.")

    new_task = Task(next_id, title.strip())
    tasks.append(new_task)
    save_tasks(tasks)

    next_id += 1
    save_next_id(next_id)

    return {"message": "Task added successfully", "task": new_task.to_dict()}

@app.put("/tasks/{task_id}")
def toggle_task(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.toggle()
            save_tasks(tasks)
            return {"message": "Task updated", "task": task.to_dict()}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            removed = tasks.pop(idx)
            save_tasks(tasks)
            return {"message": "Task deleted", "task": removed.to_dict()}
    raise HTTPException(status_code=404, detail="Task not found")
