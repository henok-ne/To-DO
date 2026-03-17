from dataclasses import dataclass
@dataclass
class Task:
    id: int
    title:str
    completed:bool=False
    def complete(self):
        self.completed=True
    def toggle(self):
        self.completed = not self.completed
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed
        }

