# Task Management API (FastAPI)
This is a RESTful backend API that allows authenticated users to manage their personal tasks.

## Features

- User Registration and Login (JWT Authentication)
- Password hashing using bcrypt
- Protected task routes
- Create, Read, Update, Delete tasks
- Task ownership enforcement
- PostgreSQL database integration

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Passlib (bcrypt)
- Python-JOSE (JWT)
-Docker & Docker Compose

## API Endpoints

POST /signup  
POST /login  
GET /tasks  
PUT /tasks/{task_id}  
DELETE /tasks/{task_id}

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone <your-repo-link>
cd <your-project-folder>

2. Install dependencies
```bash
pip install -r requirements.txt
3. Start PostgreSQL

Make sure PostgreSQL is running locally.

4. Run the server
```bash
uvicorn main:app --reload

5. Open API docs
```bash
http://127.0.0.1:8000/docs

🐳 Docker Setup

Run the full system (FastAPI + PostgreSQL):
```bash
docker-compose up --build
```bash
Then open:
http://localhost:8000/docs

🌐 Live Deployment

The API is deployed and accessible online:

👉 https://your-render-link.onrender.com/docs

Author

Henok Mesfin
Backend Developer (FastAPI / Python)

GitHub: https://github.com/henok-ne

📈 Future Improvements
Pagination for tasks
Task deadlines and priorities
User roles (admin / standard)
Refresh tokens for authentication
Rate limiting
Improved error handling
