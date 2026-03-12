import json
from struct12 import Task

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


def add_task(task, tasks):
    if not task.strip():
        print("Task cannot be empty.")
        return

    # new_task = {
    #     "title": task.strip(),
    #     "completed": False
    # }
    new_task = Task(task.strip())

    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully.")


def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\nYour Tasks:")
    for idx, task in enumerate(tasks, start=1):
        status = "✓ Completed" if task.completed else "✗ Not Completed"
        print(f"{idx}. {task.title} [{status}]")
    print()


def edit_task(tasks):
    if not tasks:
        print("Nothing to edit.")
        return

    view_tasks(tasks)

    try:
        number = int(input("Enter task number to toggle completion: "))
        index = number - 1

        if index < 0 or index >= len(tasks):
            print("Invalid task number.")
            return

        # Toggle completion status
        tasks[index].toggle()
        save_tasks(tasks)

        print("Task updated successfully.")

    except ValueError:
        print("Please enter a valid number.")


def delete_task(tasks):
    if not tasks:
        print("Nothing to delete.")
        return

    view_tasks(tasks)

    try:
        number = int(input("Enter task number to delete: "))
        index = number - 1

        if index < 0 or index >= len(tasks):
            print("Invalid task number.")
            return

        removed = tasks.pop(index)
        save_tasks(tasks)

        print(f"'{removed['title']}' deleted successfully.")

    except ValueError:
        print("Please enter a valid number.")


def main():
    tasks = load_tasks()

    while True:
        command = input(
            "Enter command (add/view/edit/delete/exit): "
        ).strip().lower()

        if command == "add":
            task = input("Enter task: ")
            add_task(task, tasks)

        elif command == "view":
            view_tasks(tasks)

        elif command == "edit":
            edit_task(tasks)

        elif command == "delete":
            delete_task(tasks)

        elif command == "exit":
            print("Exiting program.")
            break

        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()