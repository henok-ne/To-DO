from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import declarative_base,sessionmaker

engine=create_engine("postgresql://postgres:0@localhost:5432/todo_db")

Base=declarative_base()

class Task(Base):
    __tablename__="tasks"

    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    completed=Column(Boolean,default=False)

Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
db=Session()

new_task=Task(title="bhvbj")
db.add(new_task)
db.commit()

tasks=db.query(Task).filter(Task.completed==True).all()

for task in tasks:
    print(f"ID: {task.id}, Title: {task.title}, Completed: {task.completed}")

db.close()