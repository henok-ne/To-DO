class Task:
    def __init__(self,title):
        self.title=title
        self.completed=False
    def complete(self):
        self.completed=True
    def toggle(self):
        self.completed = not self.completed
    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed
        }


task1=Task("Go to the gym")
print(task1.title)
task2=Task("Go to the park")
print(task2.title)