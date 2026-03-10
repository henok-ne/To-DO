from storage import save_tasks
def add_task(task, tasks):
    if not task.strip():
        print("Task cannot be empty.")
        return

    new_task = {
        "title": task.strip(),
        "completed": False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully.")


def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\nYour Tasks:")
    for idx, task in enumerate(tasks, start=1):
        status = "✓ Completed" if task["completed"] else "✗ Not Completed"
        print(f"{idx}. {task['title']} [{status}]")
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
        tasks[index]["completed"] = not tasks[index]["completed"]
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