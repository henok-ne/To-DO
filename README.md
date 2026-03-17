# FastAPI To-Do API 🚀

This is a professional version of my Python To-Do project, now built as a REST API using FastAPI.  

It demonstrates:

- Structured data with Pydantic models
- CRUD operations (Create, Read, Update, Delete)  
- JSON persistence
- Unique IDs for tasks  
- Error handling and validation
- Clean, production-ready API responses  

---

🛠️ Features

1. Add Task 
   - POST `/tasks`  
   - JSON body example:  
   
json

            {
              "title": "Study Python",
              "completed": false
            }
   
2. View All Tasks
   
    GET /tasks
   
Returns all tasks in structured JSON

3. Update Task Completion
   
     PUT /tasks/{task_id}
   
JSON body example:

json

         {
           "completed": true
         }

4. Delete Task
   
   DELETE /tasks/{task_id}

Removes a task by its unique ID

   📝 Task Model
Tasks are represented using a dataclass:
Python
@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
Each task has a unique ID, title, and completion status.

💻 How to Run
1. Clone this repository:
   
            git clone <your-repo-url>
            cd <repo-folder>

3. Create a virtual environment (recommended):
            python -m venv venv

4. Activate the environment:
  Windows PowerShell:

            venv\Scripts\Activate.ps1
   Windows CMD:
   
            venv\Scripts\activate.bat
   Mac/Linux:
   
            source venv/bin/activate
6. Install dependencies:
   
           pip install fastapi uvicorn
8. Run the API:
   
            uvicorn main:app --reload
10. Open your browser at
    
            http://127.0.0.1:8000/docs⁠ to see Swagger UI and test the endpoints.
    
📌 Key Learnings

Difference between query parameters and request body.

Using Pydantic models for input validation.

Handling errors gracefully with HTTPException.

Unique IDs management using a separate JSON file.

Converting a CLI project into a professional backend API.
