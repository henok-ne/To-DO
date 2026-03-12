from fastapi import FastAPI, HTTPException
import json
import os
from struct12 import Task 

app = FastAPI()
filepath = "tasks.json"


def load_tasks():
    """Load tasks from JSON file and convert to Task objects."""
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            tasks = []
            for item in data:
                task = Task(title=item["title"])
                task.completed = item.get("completed", False)
                tasks.append(task)
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    """Save list of Task objects to JSON file."""
    with open(filepath, "w") as file:
        json.dump([t.to_dict() for t in tasks], file, indent=4)



@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API!"}

@app.get("/tasks")
def get_tasks():
    tasks = load_tasks()
    return {"tasks": [t.to_dict() for t in tasks]}


@app.post("/tasks")
def add_task(task_title: str):
    if not task_title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")
    
    tasks = load_tasks()
    new_task = Task(title=task_title.strip())
    tasks.append(new_task)
    save_tasks(tasks)
    
    return {"message": "Task added successfully", "task": new_task.to_dict()}


@app.put("/tasks/{task_id}")
def toggle_task(task_id: int):
    tasks = load_tasks()
    
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks[task_id].toggle()
    save_tasks(tasks)
    
    return {"message": "Task updated successfully", "task": tasks[task_id].to_dict()}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    removed_task = tasks.pop(task_id)
    save_tasks(tasks)
    
    return {"message": "Task deleted successfully", "task": removed_task.to_dict()}