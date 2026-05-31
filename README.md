# KanMind Backend

**KanMind** is a Kanban board application designed for team-based task management. This repository contains the **Django REST Framework backend**.

> This project is a **learning project** and my first self-developed backend application. It was created as part of my software development training.

The corresponding frontend can be found here:
**KanMind Frontend:** https://github.com/croser93/KanMind_FrontEnd.git

---

## Table of Contents

* [Technologies](#technologies)
* [Features](#features)
* [Project Structure](#project-structure)
* [Installation & Setup](#installation--setup)
* [Demo Users](#demo-users)
* [Author](#author)

---

## Technologies

| Technology            | Version    |
| --------------------- | ---------- |
| Python                | 3.14.4     |
| Django                | 6.0.4      |
| Django REST Framework | 3.17.1     |
| SQLite3               | File-based |
| django-cors-headers   | 4.9.0      |

---

## Features

* User registration and login with token authentication
* Create, update, and delete boards
* Add members to boards
* Create tasks with status, priority, due date, assignee, and reviewer
* Add comments to tasks
* Retrieve assigned tasks and review tasks
* Role-based permission system (Owner, Assignee, Reviewer)

---

## Project Structure

```text
KanMind_BackEnd/
├── core/               # Django project configuration (settings, urls)
├── auth_app/           # Registration, login, logout
├── board_app/          # Board management and members
├── task_app/           # Tasks and comments
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/croser93/KanMind_BackEnd.git
```

### 2. Navigate to the project directory

```bash
cd KanMind_BackEnd
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create migration files

```bash
python manage.py makemigrations
```

### 7. Apply migrations

```bash
python manage.py migrate
```

### 8. Start the development server

```bash
python manage.py runserver
```

The server will then be available at:

```text
http://127.0.0.1:8000/
```

---

## Demo Users

Create demo users for testing the application.

Start the Django shell:

```bash
python manage.py shell
```

Then paste the following code:

```python
from django.contrib.auth.models import User

customer = User.objects.create_user(username='andrey',password='asdasd',email='andrey@test.com')
business = User.objects.create_user(username='kevin',password='asdasd24',email='kevin@test.com')
```

---

## Author

**Maik G.**

Frontend Developer currently expanding into Full-Stack Development. This project was created as part of my training at Developer Akademie.
