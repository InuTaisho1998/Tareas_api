# Tareas API

[![CI Status](https://github.com/InuTaisho1998/Tareas_api/actions/workflows/ci.yml/badge.svg)](https://github.com/InuTaisho1998/Tareas_api/actions)
![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

REST API for managing tasks, developed as a backend practice project.

The main objective of this project is to practice the fundamentals of backend development: building HTTP endpoints, handling requests and responses, working with persistent data, validating input, and organizing a small API in a maintainable way.

> This project is part of my backend development portfolio and represents an early-stage project focused on learning and applying core backend concepts.

---

## 🚀 Features

* Login user
* Register user
* Create tasks
* Get tasks
* Get a task by ID
* Get a all tasks
* Update tasks
* Delete tasks
* Request validation
* HTTP status code handling
* Persistent data storage
* RESTful API structure

---

## 🛠️ Technologies

The project is currently built with:

* **python**
* **FastAPI**
* **postgresql**
* **authentication**

### Main concepts practiced

* REST API development
* CRUD operations
* HTTP methods and status codes
* Input validation
* Error handling
* Separation of responsibilities
* Database interaction
* Git and GitHub workflow

---

## 📁 Project Structure

```text
Tareas_api/
│
├── [app]/
│   ├── [router]
│   │   ├── [auth.py]
│   │   └── [task.py]
│   ├── [database.py]
│   ├── [main.py]
│   ├── [config.py]
│   ├── [models.py]
│   ├── [security.py]
│   └── [schemas.py]
│
├── [tests]/
│   ├── [api]/
│   │   └── [test_api.py]
│   ├── [unit]/
│   │   └── [test_unit.py]
│   └── conftest.py
│
├── docker-compose.yml
├── README.md
├── .dockerignore
├── .gitignore
├── requirements.txt
└── [Dockerfile]
```

The project is intentionally kept relatively simple. The goal is to demonstrate a clear understanding of backend fundamentals rather than introduce unnecessary complexity.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/InuTaisho1998/Tareas_api
```

### 2. Enter the project directory

```bash
cd Tareas_api
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file when required by the project.
But it have already some variables set

Example:

```env
SECRET_KEY=misupersecretkey
POSTGRES_USER=postgresuser
POSTGRES_PASSWORD=Fakepassword
```

> Do not commit real credentials, passwords, API keys, or other sensitive information to the repository.

### 5. Run the application

```bash
docker compose up --build
```

The API should then be available at:

```text
http://localhost:8000
```

---

## 📡 API Endpoints

### Tasks

| Method          | Endpoint                   | Description       |
| --------------- | -------------              | ----------------- |
| `GET`           | `/api/v1/tasks`            | Get all tasks     |
| `GET`           | `/api/v1/tasks{task_id}`   | Get a task by ID  |
| `POST`          | `/api/v1/tasks`            | Create a newtask |
| `PUT` / `PATCH` | `/api/v1/tasks{task_id}`   | Update atask     |
| `DELETE`        | `/api/v1/tasks{task_id}`   | Delete atask     |

> Update this table to match the routes implemented in the project.

---

## 📝 Example Request

### Create a task

```http
POST /tasks
Content-Type: application/json
```

```json
{
  "title": "Study backend development",
  "description": "Practice REST APIs and database operations"
}
```

### Example response

```json
{
  "id": 1,
  "title": "Study backend development",
  "description": "Practice REST APIs and database operations"
}
```

The exact request and response structure depends on the implementation of the API.

---

## 🔎 API Documentation

When running the project locally, API endpoints can be tested using tools such as:

* **Postman**
* **Insomnia**
* **curl**
* **[Swagger/OpenAPI, if implemented]**

Example:

```text
http://localhost:8000/docs
```

---

## ✅ What I Learned

This project was created to strengthen my understanding of backend development through a small but complete API.

During its development, I practiced:

* Creating REST endpoints
* Using HTTP methods correctly
* Working with CRUD operations
* Validating incoming data
* Handling common API errors
* Connecting an application to a database
* Organizing backend code
* Using Git for version control
* Documenting a project for other developers

---

## 🔧 Possible Improvements

This project is intentionally simple, but there are several areas that could be improved as I continue developing my backend skills:

* Add automated tests
* Add better centralized error handling
* Improve logging
* Improve database migrations
* Add pagination and filtering for larger datasets

These improvements are part of the project's learning path rather than requirements for its current version.

---

## 🎯 Project Scope

This is a **junior-level backend project** created to demonstrate the ability to build and organize a basic REST API.

It is not intended to be presented as a production-ready system. Instead, it serves as a foundation for progressively more advanced projects involving authentication, testing, architecture, deployment, and scalability.

---

## 📌 Project Status

**Status:** In development / learning project

The project may evolve as new backend concepts are learned and applied.

---

## 👨‍💻 Author

**InuTaisho1998**

GitHub:
https://github.com/InuTaisho1998

---

#---

## 📄 License

This project is licensed under the [MIT License](LICENSE).