from storage import load_tasks
from tasks import add_task, view_tasks, edit_task, delete_task
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