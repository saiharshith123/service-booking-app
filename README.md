# CarePoint — Service Booking Full-Stack Application

A responsive clinic/service-center appointment system built with React, FastAPI and PostgreSQL.

## Features
- Customer registration and login with signed JWT access tokens.
- Password hashing with Argon2.
- Customer role and administrator role checks.
- Browse future appointment slots and book one available slot.
- View personal booking history, cancel and reschedule.
- Admin can create/deactivate slots and view/cancel all bookings.
- PostgreSQL schema managed by Alembic.
- Swagger UI at `/docs`, health endpoint at `/health`.
- Responsive frontend with semantic labels and accessible status messages.

## Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL 14+
- Git (optional)

## 1. Create PostgreSQL database
Open pgAdmin Query Tool or `psql` and run:
```sql
CREATE DATABASE service_booking;
```

## 2. Start backend (Windows PowerShell)
```powershell
cd service-booking-appackend
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and set your PostgreSQL username/password and a long random `SECRET_KEY`.
Example:
```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/service_booking
SECRET_KEY=replace-this-with-a-long-random-secret-value
ACCESS_TOKEN_EXPIRE_MINUTES=60
FRONTEND_ORIGIN=http://localhost:5173
```
Run migrations and create the first admin:
```powershell
alembic upgrade head
python -m app.seed_admin
uvicorn app.main:app --reload
```
Backend: http://localhost:8000  
Swagger: http://localhost:8000/docs  
Health: http://localhost:8000/health

Admin demo account (change password / secret before real use):
- Email: `admin@clinic.com`
- Password: `Admin12345!`

## 3. Start frontend (new terminal)
```powershell
cd service-booking-approntend
npm install
Copy-Item .env.example .env
npm run dev
```
Open http://localhost:5173

## 4. First-time test flow
1. Sign in as `admin@clinic.com`.
2. Open Admin in the navigation.
3. Create a future slot (start and end times).
4. Log out.
5. Register a normal customer account.
6. Book the slot from Available appointments.
7. Open My bookings and test reschedule/cancel.
8. Sign back in as admin to inspect all bookings.

## 5. API overview
| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Register customer |
| POST | `/api/auth/login` | Public | Obtain JWT |
| GET | `/api/auth/me` | Logged in | Current user |
| GET | `/api/slots` | Public | List upcoming slots |
| POST | `/api/slots` | Admin | Create slot |
| PATCH | `/api/slots/{id}/deactivate` | Admin | Deactivate slot |
| POST | `/api/bookings` | Logged in | Book slot |
| GET | `/api/bookings/mine` | Logged in | Own booking history |
| PATCH | `/api/bookings/{id}/cancel` | Owner/Admin | Cancel booking |
| PATCH | `/api/bookings/{id}/reschedule` | Owner/Admin | Reschedule booking |
| GET | `/api/bookings` | Admin | All bookings |

Use Swagger's **Authorize** button and paste the JWT access token (without quotes). The API uses HTTP Bearer authentication, so Swagger adds the `Bearer` prefix.

## 6. Run tests
Backend:
```powershell
cd backend
pytest -q
```
Frontend production build:
```powershell
cd frontend
npm run build
```
Frontend component test: `npm test` (Vitest + React Testing Library).

## Database design
- `users`: identity, unique email, password hash and role.
- `slots`: service name, start/end time, location and active flag.
- `bookings`: customer FK, slot FK, status and notes.
- `uq_active_booking_slot` is a PostgreSQL partial unique index on `slot_id` for confirmed bookings only. It prevents double-booking while allowing a cancelled slot to be booked again.

## Security and production notes
- Never commit `.env`; use a strong random `SECRET_KEY`.
- The demo admin password is for local setup only. Change it before sharing/deploying.
- For production, prefer short-lived access tokens plus refresh-token rotation in secure HttpOnly cookies, HTTPS, rate limiting, audit logging, structured logging, backups and secrets management.
- This starter stores the access token in localStorage for ease of local learning. For a production deployment, move to an HttpOnly Secure SameSite cookie design and add CSRF protection where appropriate.
- Add pagination, timezone policy, email notifications, admin user management and stronger concurrent-booking integration tests before production use.
