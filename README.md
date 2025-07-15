# tasket

Tasket is a simple FastAPI task tracker, that allows user to log in and manage his tasks or create new.

---

## Table of Contents

* [Solution Overview](#solution-overview)
* [Architecture Highlights](#architecture-highlights)
* [Installation and Launch](#installation-and-launch)
* [Technologies](#technologies)
* [TODO](#todo)

---

## Solution Overview

Tasket offers a minimalist way to manage tasks:

* Create and manage tasks via API
* All data stored in PostgreSQL
* Support for asynchronous request and task handling
* Docker and tests for stability


---

## Architecture Highlights

The project is built with a focus on clean architecture and separation of concerns between layers. This ensures modularity, maintainability, and reuse of logic.

### 1. Business Logic (`core/`)

All domain logic (handling tasks and users) resides in services within the core/ layer.
This layer is fully isolated from the web and database making it easy to test and reuse when scaling.

### 2. Data Layer (`db/`)

Handles interaction with the postgres database using async SQLAlchemy.
It defines models, sessions, and schema initialization. DB logic is strictly separated from other code.

### 3. API Interface (`api/`)

Built on FastAPI. This layer serves as an adapter between the outside world and business logic:

* Endpoints (routes)
* Dependencies and authorization (JWT)
* Data serialization/deserialization
* Error handling

### 4. Docker Environment

The project is run using docker-compose, which includes the following services:

* FastAPI application
* PostgreSQL database

Containers are isolated and communicate over a Docker network.

---

## Installation and Launch

1. Clone the project:
   ```bash
   git clone https://github.com/neklyudovv/tasket.git
   cd tasket
   ```

2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the .env file based on .env.example

4. Run the project:
   ```bash
   docker-compose up --build
   ```
   
5. The API will be available at:
   ```
   http://127.0.0.1:8000/
   ```
---

## Technologies

* **FastAPI** - asynchronous Python framework
* **PostgreSQL** - database
* **SQLAlchemy** (async) - ORM
* **Docker** - project deployment
* **JWT** - authentication and security
* **Pytest** - testing

---

## TODO

* [ ] Recurring tasks (daily, weekly)
* [ ] Frontend web interface
* [ ] Editing task time/content