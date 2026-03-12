from dataclasses import dataclass
class Task:
    title:str
    completed:bool=False
    def complete(self):
        self.completed=True
    def toggle(self):
        self.completed = not self.completed
    def to_dict(self):
        return {
            "title": self.title,
            "completed": self.completed
        }

