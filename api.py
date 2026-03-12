from fastapi import FastAPI, HTTPException
import json
import os
app = FastAPI()
filepath="tasks.json"
@app.get("/")
def home():
    return {"message": "Welcome to the To-Do API!"}

#load tasks from json file
def load_tasks():
    if not os.path.exists(filepath):
        return []
    with open(filepath,"r") as file:
        return json.load(file)
    
#save tasks to json file
def save_tasks(tasks):
    with open(filepath,"w") as file:
        json.dump(tasks,file,indent=4)

@app.get("/tasks")
def get_tasks():
    tasks=load_tasks()
    return {"tasks":tasks}

@app.post("/tasks")
def add_task(task: str):
    tasks=load_tasks()
    new_task={
        "title":task,
        "completed":False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return {"message":"Task added successfully."}

@app.put("/tasks/{task_id}")
def toggle_task(task_id: int):
    tasks = load_tasks()
    
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Toggle the completed status
    tasks[task_id]["completed"] = not tasks[task_id]["completed"]
    save_tasks(tasks)
    
    return tasks[task_id]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    
    if task_id < 0 or task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    
    removed_task = tasks.pop(task_id)  
    save_tasks(tasks)
    
    return {"message": "Task deleted successfully", "task": removed_task}