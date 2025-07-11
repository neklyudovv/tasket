# tasket

**Tasket** is a task tracker with Telegram bot integration that reminds users about deadlines and tasks. Users can create and manage tasks via Telegram or the web interface.

---

## Table of Contents

* [Solution Overview](#solution-overview)
* [Architecture Highlights](#architecture-highlights)
* [Installation and Launch](#installation-and-launch)
* [Technologies](#technologies)
* [TODO](#todo)

---

## Solution Overview

**Tasket** offers a minimalist way to manage tasks:

* Create and manage tasks via API or Telegram bot
* Scheduled reminders
* All data stored in PostgreSQL
* Support for asynchronous request and task handling
* Docker and tests for stability

The Telegram bot is a client for API - it's a full-featured interaction channel, including interactive reminders and task management.

Reminders are scheduled using `APScheduler`: when a task is created, a job is registered in the system to send a notification at the appropriate time.

---

## Architecture Highlights

The project is built with a focus on **clean architecture** and **separation of concerns** between layers. This ensures modularity, maintainability, and reuse of logic.

### 1. **Business Logic (`backend/core/`)**

All domain logic (handling tasks, reminders, and users) resides in services within the `core/` layer.
This layer is fully isolated from the web, database, and Telegram API, making it easy to test and reuse when scaling.

### 2. **Data Layer (`backend/db/`)**

Handles interaction with the database using async `SQLAlchemy`.
It defines models, sessions, and schema initialization. DB logic is strictly separated from other code.

### 3. **API Interface (`backend/api/`)**

Built on `FastAPI`. This layer serves as an adapter between the outside world and business logic:

* Endpoints (routes)
* Dependencies and authorization (JWT)
* Data serialization/deserialization
* Error handling

### 4. **Telegram Bot (acts as an API client)**

Implemented using `Aiogram`, the Telegram bot acts as an **external client**, sending HTTP requests to the REST API:

* Creating and deleting tasks
* Retrieving user tasks
* Marking tasks as completed
* Sending reminders at scheduled times

The bot has no knowledge of the `core` layer and does not use services directly.
This makes the architecture flexible: additional clients (e.g., web or mobile) can be added without changing core logic.

### 5. **Scheduler**

Reminders are managed using `APScheduler`.
When a task is created via the API, the scheduler registers a deferred action to notify the user via the Telegram bot or a separate service.

### 6. **Docker Environment**

The project is run using `docker-compose`, which includes the following services:

* FastAPI application
* Telegram bot
* PostgreSQL database

Containers are isolated and communicate over a Docker network.

---

## Installation and Launch

1. Clone the project:

   ```bash
   git clone https://github.com/neklyudovv/tasket.git
   cd tasket
   ```

2. Set up the `.env` file based on `.env.example`

3. Run the project:

   ```bash
   docker-compose up --build
   ```

4. The API will be available at:

   ```
   http://127.0.0.1:8000/
   ```

---

## Technologies

* **FastAPI** - asynchronous Python framework
* **SQLAlchemy** (async) - ORM
* **PostgreSQL** - database
* **APScheduler** - task scheduler
* **aiogram** - asyncio-based Telegram bot framework
* **Docker** - project deployment
* **JWT** - authentication and security
* **Pytest** - testing

---

## TODO

* [ ] Recurring tasks (daily, weekly)
* [ ] Frontend web interface
* [ ] Multiple reminders before deadline
* [ ] Flexible notification scheduling
* [ ] Editing task time/content