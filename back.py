with open("tasks.txt","r") as file:
    content=file.readlines()

print(content)

with open("tasks.txt","w") as file:
    file.write("study\n")
    file.write("code\n")