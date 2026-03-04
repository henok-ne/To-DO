import json

def load_tasks(tasks):
    try:
        with open("tasks.json","r") as file:
                tasks.extend(json.load(file))
    except FileNotFoundError:
        print("No existing tasks found. Starting fresh.")

def save_tasks(tasks): 
    with open("tasks.json","w") as file:
        json.dump(tasks,file)

def add_task(task, tasks):
    if task=="":
        print("task can't be empty")
        return
    val={
        "title":task,
        "completed":False
        }
    tasks.append(val)
    save_tasks(tasks)
    print("Added successfully")

def view_task(tasks):
    if not tasks:
        print("No tasks available.")
        return
    
    for idx, task in enumerate(tasks, start=1):
        print(idx,task["title"],task["completed"])

def edit_task(tasks):
    if not tasks:
        print("Nothing to edit.")
        return

    view_task(tasks)

    try:
        info = int(input("Enter task number to edit: "))
        idx = info - 1

        if idx < 0 or idx >= len(tasks):
            print("Invalid number.")
        else:
            new_completed = input("Enter new completion status (True/False): ").strip().lower() == "true"
            tasks[idx]["completed"] = new_completed
            save_tasks(tasks)
            print(f"Task {info} updated successfully.")

    except ValueError:
        print("Please enter a valid number.")

def dele_task(tasks):
    if not tasks:
        print("Nothing to delete.")
        return

    view_task(tasks)

    try:
        info = int(input("Enter task number to delete: "))
        idx = info - 1

        if idx < 0 or idx >= len(tasks):
            print("Invalid number.")
        else:
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"{removed} deleted successfully")

    except ValueError:
        print("Please enter a valid number.")



def main():
       tasks = []
       load_tasks(tasks)
       
       while True:
        command = input("Enter command (add/view/delete/exit): ").strip().lower()

        if command == "add":
            task = input("Enter task: ")
            add_task(task,tasks)
        elif command == "view":
            view_task(tasks)
        elif command == "edit":
            edit_task(tasks)
        elif command == "delete":
            dele_task(tasks)
        elif command == "exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()