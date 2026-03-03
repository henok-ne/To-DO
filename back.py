# with open("tasks.json","r") as file:
#     content=file.readlines()

# print(content)

# with open("tasks.json","w") as file:
#     file.write('{"tiltle":"study234567","completed":"false"}'+ "\n")
#     # file.write("code\n")



import json
# movies = [
#     {"name": "Matrix", "watched": False},
#     {"name": "Avatar", "watched": True}
# ]

# with open("tasks.json", "w") as file:
#     json.dump(movies, file)

# with open("tasks.json", "r") as file:
#     loaded_movies = json.load(file)

def load_tasks(tasks):
    try:
        with open("tasks.json","r") as file:
                tasks=list(json.load(file))
    except FileNotFoundError:
        print("No existing tasks found. Starting fresh.")


def view_task(tasks):
    if not tasks:
        print("No tasks available.")
        return
    
    for idx, task in enumerate(tasks, start=1):
        print(idx,".",task["title"],",",task["completed"])

def main():
       tasks = []
       load_tasks(tasks)
       
       while True:
        command = input("Enter command (add/view/delete/exit): ").strip().lower()

        if command == "view":
            view_task(tasks)
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
