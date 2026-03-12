import json
def load_tasks():
    """Load tasks from JSON file safely."""
    try:
        with open("tasks.json", "r") as file:
            data= json.load(file)
            tasks = []

            for item in data:
                task = Task(item["title"])
                task.completed = item["completed"]
                tasks.append(task)

        return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    """Save tasks to JSON file."""
    data=[]
    for task in tasks:
        data.append(task.to_dict())
    with open("tasks.json", "w") as file:
        json.dump(data, file, indent=4)