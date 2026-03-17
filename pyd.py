
from pydantic import BaseModel

class TaskModel(BaseModel):
    title: str
    completed: bool = False