# Smart School Fees Management System

A Django + DRF backend to manage students, classes, fee structures, invoices, and payments with JWT auth.

## Quickstart

1. Create and activate venv, install deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and create admin:

```bash
python manage.py migrate
export DJANGO_SUPERUSER_PASSWORD=admin123
python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

3. Start the server:

```bash
python manage.py runserver 0.0.0.0:8000
```

4. Obtain JWT token:

- POST `/api/auth/token/` with `{ "username": "admin", "password": "admin123" }`

5. Browse API endpoints (Authorization: Bearer <token>):

- `/api/academic-years/`
- `/api/terms/`
- `/api/classrooms/`
- `/api/guardians/`
- `/api/students/`
- `/api/fee-types/`
- `/api/fee-structures/`
- `/api/invoices/`
- `/api/payments/`

## Notes
- Default DB is SQLite. Switch to Postgres by editing `DATABASES` in `smartschool/settings.py`.
- Static files served by WhiteNoise in production.