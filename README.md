CLI Task Manager (Python)

A simple Command-Line Task Manager built in Python.

This project demonstrates how structured data is handled in real applications using lists, dictionaries, and JSON persistence.


Features

- Add a task
- View all tasks
- Delete a task
- Mark a task as completed
- Data is saved using JSON (persistent storage)



Concepts Practiced

- Python functions
- Lists and dictionaries (list of dictionaries pattern)
- CRUD operations (Create, Read, Update, Delete)
- JSON serialization and deserialization (json.dump / json.load)
- Exception handling (FileNotFoundError, JSONDecodeError)
- Understanding mutation vs reassignment in functions



Key Learning Concept

One important concept learned in this project:

Difference between modifying a parameter and returning a value.**

Example:

Reassignment (does NOT modify original list):
def load_tasks(tasks):
    tasks = json.load(file)
This creates a new list and does not affect the original list outside the function.

Mutation (modifies original list):def load_tasks(tasks):
    tasks.clear()
    tasks.extend(json.load(file))
This modifies the same list object.
Better design approach:
def load_tasks():
    return json.load(file)
Returning the data makes the function independent and cleaner.

Rule learned:
- If a function's job is to GET data → return it.
- If a function's job is to DO something → perform the action without returning.

How to Run

1. Clone the repository
2. Navigate to the project folder
3. Run:

python To-Do.py
