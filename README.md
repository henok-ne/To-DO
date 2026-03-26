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

## API Endpoints

POST /signup  
POST /login  
GET /tasks  
PUT /tasks/{task_id}  
DELETE /tasks/{task_id}

## How to Run

1. Clone the repository
2. Install dependencies:
            ``` pip install requirements.txt ```
3. Start PostgreSQL
4. Run server:
     ```uvicorn main:app --reload```

## Future Improvements

- Docker containerization
- Deployment to cloud platform
- Pagination
- Task deadlines
- User roles

