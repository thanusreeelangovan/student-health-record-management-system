# MediCampus — Full-Stack Student Health Record Management System

> Upgraded from your Tkinter desktop app → Full-stack web application

## Tech Stack
- **Backend:** Python + Flask REST API
- **Database:** SQLite (auto-created, no setup needed)
- **Frontend:** Vanilla JS + HTML/CSS (single-page app)
- **Auth:** JWT-based login/signup

## Project Structure
```
healthsystem/
├── app.py              ← Flask backend + all API routes
├── requirements.txt    ← Python dependencies
├── health.db           ← SQLite DB (auto-created on first run)
└── frontend/
    └── index.html      ← Full SPA frontend (served by Flask)
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/login | Login |
| POST | /api/signup | Register |
| GET | /api/patients | List all patients |
| GET | /api/patients?q=search | Search patients |
| POST | /api/patients | Add patient |
| GET | /api/patients/:id | Patient + records |
| PUT | /api/patients/:id | Update patient |
| DELETE | /api/patients/:id | Delete patient |
| POST | /api/records | Add health record |
| GET | /api/appointments | List appointments |
| POST | /api/appointments | Book appointment |
| PUT | /api/appointments/:id | Update status |
| GET | /api/analytics | Dashboard analytics |

## Quick Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
python app.py
```

### 3. Open browser
```
http://localhost:5000
```

### 4. Login with demo account
- **Email:** doctor@school.com
- **Password:** doctor123

## Features
-  JWT Login / Signup system
-  Patient CRUD (Add, View, Update, Delete)
-  Health records per patient (diagnosis, vitals, medications)
-  Appointment booking & status management
-  Doctor dashboard with live stats
-  Analytics with 4 chart types (Bar, Line, Doughnut, Polar)
-  Search & filter patients
-  Pre-seeded demo data (8 students, 10 health records)
-  Responsive dark UI

## Upgrade Path
To connect to MySQL instead of SQLite, replace `sqlite3` with `mysql-connector-python`
and update `get_db()` connection string.

Built by: Thanusree E — MVJ College of Engineering
