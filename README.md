# tasket

Tasket is a simple FastAPI task tracker, that allows user to log in and manage his tasks or create new.

---

## Table of Contents

* [Technologies](#technologies)
* [Solution Overview](#solution-overview)
* [Architecture Highlights](#architecture-highlights)
* [Installation and Launch](#installation-and-launch)
* [TODO](#todo)

---

## Technologies

* **FastAPI** - asynchronous Python framework
* **Docker** - project deployment
* **Github Actions** - CI/CD
* **PostgreSQL** - database
* **SQLAlchemy** (async) - ORM
* **Alembic** - database migrations
* **Pydantic v2** - data validation and settings management
* **SlowAPI** - rate limiting
* **JWT** - authentication and security
* **Pytest** - integration and unit testing

## Solution Overview

Tasket offers a minimalist way to manage tasks:

* Create and manage tasks via API
* All data stored in PostgreSQL
* Support for asynchronous request and task handling
* Docker and tests for stability


---

## Architecture Highlights

The project is built with a focus on clean architecture and separation of concerns between layers. This ensures modularity, maintainability, and reuse of logic.

### 1. Business Logic (`services/`)

All business logic (handling tasks and users) resides in **services**.

### 2. API Interface (`api/`)

Built on **FastAPI**. This layer serves as an adapter between the outside world and business logic:

* Endpoints (routers)
* Dependencies and authorization (JWT)
* Rate limiting (SlowAPI)
* Error handling

### 3. Configuration (`core/`)

Contains application configuration (environment variables) and core exceptions.

### 4. Data Models (`schemas/`)

Pydantic models / schemas used for validation and serialization.

### 5. Data Layer (`db/`)

Handles interaction with the postgres database using async SQLAlchemy.
It defines models, sessions, and schema initialization. DB logic is strictly separated from other code.

### 6. Database Migrations (`alembic/`)

Database schema versions are managed using **Alembic**. This ensures that all changes to the database structure are tracked and applied potentially without downtime.

### 7. Docker Environment

The project uses **docker-compose** to run the following services:

* FastAPI application
* PostgreSQL database

Containers are isolated and communicate over a Docker network.

---

## API Endpoints

### Authentication
* `POST /users/register` - Register a new user
* `POST /users/login` - Login and get access token

### Tasks
* `GET /tasks/` - Get list of tasks
* `POST /tasks/` - Create a new task
* `GET /tasks/{task_id}` - Get a specific task
* `PATCH /tasks/{task_id}` - Update a task
* `DELETE /tasks/{task_id}` - Delete a task

---

## Installation and Launch

1. Clone the project:
   ```bash
   git clone https://github.com/neklyudovv/tasket.git
   cd tasket
   ```

2. Set up the .env file based on .env.example

3. Run the project:
   ```bash
   docker-compose up --build
   ```
   
4. API will be available at:
   ```
   http://localhost:8000/

> **Optional**
>
> Run tests:
> ```bash
> pytest
> ```
>
> **CI/CD**:
> The project uses **Github Actions** to run tests automatically on every push and pull request to `main`.
> Check `.github/workflows/ci.yml` for details.

---

## TODO

* [ ] Recurring tasks (daily, weekly)
* [ ] Frontend web interface
* [ ] Editing task time/content