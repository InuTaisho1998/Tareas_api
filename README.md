# Tareas API

REST API for managing tasks, developed as a backend practice project.

The main objective of this project is to practice the fundamentals of backend development: building HTTP endpoints, handling requests and responses, working with persistent data, validating input, and organizing a small API in a maintainable way.

> This project is part of my backend development portfolio and represents an early-stage project focused on learning and applying core backend concepts.

---

## 🚀 Features

* Create tasks
* Get tasks
* Get a task by ID
* Update tasks
* Delete tasks
* Request validation
* HTTP status code handling
* Persistent data storage
* RESTful API structure

---

## 🛠️ Technologies

The project is currently built with:

* **[YOUR LANGUAGE]**
* **[YOUR FRAMEWORK]**
* **[YOUR DATABASE]**
* **[OTHER MAIN TECHNOLOGY, IF APPLICABLE]**

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
Tareas_apihazme/
│
├── [folder]/
│   ├── [file]
│   └── [file]
│
├── [folder]/
│   ├── [file]
│   └── [file]
│
├── [configuration file]
├── README.md
└── [other important files]
```

The project is intentionally kept relatively simple. The goal is to demonstrate a clear understanding of backend fundamentals rather than introduce unnecessary complexity.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/InuTaisho1998/Tareas_apihazme.git
```

### 2. Enter the project directory

```bash
cd Tareas_apihazme
```

### 3. Install dependencies

```bash
[INSTALL COMMAND]
```

### 4. Configure environment variables

Create a `.env` file when required by the project.

Example:

```env
[VARIABLE_NAME]=[VALUE]
[VARIABLE_NAME]=[VALUE]
```

> Do not commit real credentials, passwords, API keys, or other sensitive information to the repository.

### 5. Run the application

```bash
[RUN COMMAND]
```

The API should then be available at:

```text
http://localhost:[PORT]
```

---

## 📡 API Endpoints

### Tasks

| Method          | Endpoint      | Description       |
| --------------- | ------------- | ----------------- |
| `GET`           | `/tasks`      | Get all tasks     |
| `GET`           | `/tasks/{id}` | Get a task by ID  |
| `POST`          | `/tasks`      | Create a new task |
| `PUT` / `PATCH` | `/tasks/{id}` | Update a task     |
| `DELETE`        | `/tasks/{id}` | Delete a task     |

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
http://localhost:[PORT]/[DOCS_ROUTE]
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
* Improve API validation
* Add better centralized error handling
* Add authentication and authorization
* Improve logging
* Add API documentation with OpenAPI/Swagger
* Containerize the application with Docker
* Add CI with GitHub Actions
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

## 📄 License

This project currently does not specify a license.
