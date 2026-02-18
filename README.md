# Park Ranger (Phase 1) - Ongoing

This commit contains only Phase 1 (database + environment setup).

---

## WHat's inside of this commit?

- `database.sql` (MySQL schema)
- `backend/db.py` (database connection script)
- `.env.example` (example environment variables, magcreate kayo ng sarili niyo based sa configuration niyo sa SQL)
- `requirements.txt` (Python dependencies)
- `.gitignore`


## Setup Instructions

### Import Database

1. Open **XAMPP**
(edit) Start **Apache**
2. Start **MySQL**
3. Open **phpMyAdmin using Admin button sa XAMPP MySQL**
4. Click **Import**
5. Select `database.sql`
6. Click **Go**



### Setup Environment Variables

1. Go to `backend/`
2. Copy `.env.example` to `.env`
3. Fill in your MySQL password

# Park Ranger (Phase 2)

##added

- `backend/app.py` (Flask API backend: user login, product/location/feedback CRUD, JWT authentication, and database interaction)
