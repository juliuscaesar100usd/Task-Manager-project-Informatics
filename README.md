# Task Manager

A full-stack task management web application built with **FastAPI**, **SQLite**, and vanilla **HTML/CSS/JavaScript**. Designed for workplace use where an admin (boss) manages tasks for a team of workers.

---

## Features

- **Role-based access control** — admin and worker roles with separate dashboards
- **JWT authentication** — secure login with token-based sessions
- **Admin capabilities:**
  - Create, view, update, and delete tasks for any user
  - Assign tasks to specific workers
  - View all tasks across all users in one dashboard
  - See live stats (total tasks, incomplete, complete, number of users)
- **Worker capabilities:**
  - View only tasks assigned to them
  - Update the status of their own tasks (complete / incomplete)
  - See personal stats and overdue deadline highlights
- **Task properties:** Title, Description, Status, Priority (Low / Medium / High), Deadline, Created At

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, FastAPI |
| Database | SQLite via SQLAlchemy ORM |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Server | Uvicorn |

---

## Project Structure

```
task-manager/
├── backend/
│   ├── main.py              # FastAPI app entry point + CORS
│   ├── database.py          # SQLite engine, session, Base
│   ├── models.py            # SQLAlchemy ORM models (User, Task)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── auth.py              # Password hashing + JWT logic
│   ├── dependencies.py      # get_current_user, require_admin guards
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # POST /auth/register, POST /auth/login
│       └── tasks.py         # Full task CRUD (admin) + user task routes
├── frontend/
│   ├── index.html           # Login page
│   ├── admin.html           # Admin dashboard
│   ├── user.html            # Worker dashboard
│   └── style.css            # Shared styles
├── .env                     # Secret key (NOT committed to git)
├── .gitignore
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `pip` and `venv`
- A modern web browser

On Ubuntu, make sure you have the required tools:
```bash
sudo apt install python3 python3-pip python3-venv
```

---

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create the `.env` file**

Create a file called `.env` in the project root with the following content:
```
SECRET_KEY=your_secret_key_here
```

To generate a secure secret key, run:
```bash
openssl rand -hex 32
```
Copy the output and paste it as the value of `SECRET_KEY`.

**5. Start the server**
```bash
uvicorn main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.

---

### Running the Frontend

The frontend is plain HTML and must be served — do not open files by double-clicking them in the file manager.

**Option A — VSCode Live Server (recommended)**
1. Install the **Live Server** extension in VSCode
2. Right-click `frontend/index.html`
3. Select **Open with Live Server**
4. The app opens at `http://127.0.0.1:5500/index.html`

**Option B — Python HTTP server**
```bash
cd frontend
python3 -m http.server 5500
```
Then open `http://127.0.0.1:5500` in your browser.

> Make sure the FastAPI server is also running at the same time.

---

## API Reference

Interactive API docs are available at `http://127.0.0.1:8000/docs` when the server is running (Swagger UI).

### Authentication

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/auth/register` | Public | Register a new user |
| POST | `/auth/login` | Public | Login and receive JWT token |

### Admin — Task Management

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/tasks/` | Admin | Create a task and assign to a user |
| GET | `/tasks/` | Admin | Get all tasks across all users |
| GET | `/tasks/{task_id}` | Admin | Get one task by ID |
| PUT | `/tasks/{task_id}` | Admin | Update any field of a task |
| DELETE | `/tasks/{task_id}` | Admin | Delete a task |

### Worker — Own Tasks

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/tasks/my-tasks` | Any user | Get all tasks assigned to current user |
| GET | `/tasks/my-tasks/{task_id}` | Any user | Get one of own tasks by ID |
| PATCH | `/tasks/my-tasks/{task_id}/status` | Any user | Update status of own task only |

---

## User Management

User registration is intentionally admin-controlled — workers do not self-register. This reflects a real workplace model where the boss controls who has access to the system.

**To create a new user account:**

1. Make sure the server is running
2. Go to `http://127.0.0.1:8000/docs`
3. Find `POST /auth/register`
4. Click **Try it out** and enter a username and password
5. Click **Execute**

**To make a user an admin:**

```bash
sqlite3 database.db
```
```sql
UPDATE users SET is_admin = 1 WHERE username = 'your_username';
.quit
```

---

## Task Properties

| Property | Values | Description |
|----------|--------|-------------|
| `title` | String (required) | Short name for the task |
| `description` | String (optional) | Full details |
| `status` | `incomplete` / `complete` | Current state |
| `priority` | `low` / `medium` / `high` | Urgency level |
| `deadline` | ISO datetime (required) | Due date and time |
| `assigned_to` | User ID | Which worker the task belongs to |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Secret key used to sign JWT tokens. Generate with `openssl rand -hex 32`. Never commit this. |

---

## Security Notes

- Passwords are hashed with **bcrypt** — plain passwords are never stored
- All protected routes require a valid JWT token in the `Authorization: Bearer` header
- Workers cannot access, modify, or delete tasks belonging to other users
- The `.env` file and `database.db` are excluded from version control via `.gitignore`

---

## Dependencies

Full list in `requirements.txt`. Key packages:

```
fastapi
uvicorn
sqlalchemy
python-jose[cryptography]
passlib[bcrypt]
python-multipart
python-dotenv
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## Known Limitations

- No sorting or filtering on task lists (planned for a future version)
- No pagination — all tasks are returned in a single response
- User management (listing all users) is not exposed via the API — user IDs must be known when assigning tasks
- No password reset functionality

---

## License

This project was created as a school project and is not licensed for commercial use.