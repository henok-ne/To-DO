import json
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_tasks(tasks):
    """Save tasks to JSON file."""
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)