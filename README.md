# CarePoint – Service Booking Application

A full-stack appointment booking application built using **React, FastAPI, and PostgreSQL**. The application allows customers to register, log in, browse available appointment slots, book appointments, reschedule bookings, and cancel appointments. Administrators can manage appointment slots and monitor customer bookings.

## 🚀 Features

### Customer Features
- Customer registration and login.
- JWT-based authentication.
- View available appointment slots.
- Book appointments.
- View personal booking history.
- Reschedule confirmed appointments.
- Cancel appointments.
- View appointment status.

### Admin Features
- Admin authentication.
- Create appointment slots.
- View appointment slots.
- Deactivate appointment slots.
- View all customer bookings.
- Monitor booking status.

### Backend Features
- RESTful API using FastAPI.
- PostgreSQL database integration.
- SQLAlchemy ORM.
- Alembic database migrations.
- Password hashing using Argon2.
- JWT authentication.
- Role-Based Access Control (RBAC).
- Request validation using Pydantic.
- API documentation using Swagger UI.
- Automated backend tests using Pytest.

### Frontend Features
- Responsive React user interface.
- React components and state management.
- API integration with FastAPI.
- Customer and admin dashboards.
- Appointment booking and management.

## 🛠️ Technologies Used

| Category | Technology |
|---|---|
| Frontend | React.js |
| Build Tool | Vite |
| Programming Language | JavaScript |
| Backend | Python |
| Backend Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| Authentication | JWT |
| Password Security | Argon2 |
| API Documentation | Swagger UI |
| Testing | Pytest |
| Version Control | Git and GitHub |

## 📁 Project Structure

```text
service-booking-app/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── seed_admin.py
│   │   └── routers/
│   │
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── .gitignore
└── README.md
```

*Note: The structure above illustrates the main project areas. Your actual folders may contain additional files.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following software before running the application:

- Python 3.11 or later.
- Node.js and npm.
- PostgreSQL.
- Git.
- Visual Studio Code (recommended).

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd service-booking-app
```

Replace the repository URL with your actual GitHub repository URL.

### Step 2: Create PostgreSQL Database

Open pgAdmin or PostgreSQL Query Tool and execute:

```sql
CREATE DATABASE service_booking;
```

Verify that the database has been created successfully.

### Step 3: Configure Backend

Navigate to the backend directory:

```powershell
cd backend
```

Create a Python virtual environment:

```powershell
py -3.11 -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create the environment configuration file:

```powershell
Copy-Item .env.example .env
```

Open `backend/.env` and configure:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/service_booking

SECRET_KEY=YOUR_GENERATED_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES=60

FRONTEND_ORIGIN=http://localhost:5173
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

Generate a secure JWT secret using Python:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copy the generated value into `SECRET_KEY`.

### Step 4: Run Database Migrations

Execute:

```bash
alembic upgrade head
```

This creates the required database tables.

### Step 5: Create Admin Account

Run:

```bash
python -m app.seed_admin
```

For the local development seed configuration, the default admin credentials are:

```text
Email: admin@clinic.com
Password: Admin12345!
```

Change these credentials before using the application outside local development.

### Step 6: Start FastAPI Backend

Run:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### Step 7: Start React Frontend

Open a second terminal and navigate to the frontend directory:

```powershell
cd frontend
```

Install dependencies:

```bash
npm install
```

Create the frontend environment file if your project uses one:

```powershell
Copy-Item .env.example .env
```

Start the React development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

The application is now ready to use.

## 🔐 Authentication and Authorization

The application uses JSON Web Tokens (JWT) for authentication.

### Authentication Workflow

1. Customer registers an account.
2. Customer logs in with email and password.
3. Backend validates the credentials.
4. Backend generates an access token.
5. Frontend uses the token for authenticated API requests.
6. Backend verifies the token before allowing access to protected endpoints.

### Role-Based Access Control

| Role | Permissions |
|---|---|
| Customer | View slots, book appointments, view bookings, reschedule and cancel own bookings |
| Admin | Manage slots and view all customer bookings |

## 📡 API Endpoints

Base URL:

```text
http://127.0.0.1:8000
```

### Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register customer |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Get current user |

### Appointment Slot APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/slots` | View available slots |
| POST | `/api/slots` | Create appointment slot (Admin) |
| PATCH | `/api/slots/{id}/deactivate` | Deactivate slot (Admin) |

### Booking APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/bookings` | Create booking |
| GET | `/api/bookings/mine` | View customer bookings |
| PATCH | `/api/bookings/{id}/cancel` | Cancel booking |
| PATCH | `/api/bookings/{id}/reschedule` | Reschedule booking |
| GET | `/api/bookings` | View all bookings (Admin) |

## 🧪 Application Testing

### Customer Workflow

1. Register a new customer account.
2. Login using customer credentials.
3. Browse available appointment slots.
4. Select an appointment.
5. Book the appointment.
6. Navigate to My Bookings.
7. Verify booking details.
8. Reschedule the appointment to another available slot.
9. Verify the updated appointment.
10. Cancel an appointment.
11. Verify the cancelled status.

### Admin Workflow

1. Login using admin credentials.
2. Navigate to the Admin dashboard.
3. Create appointment slots.
4. View existing slots.
5. View customer bookings.
6. Verify booking statuses.
7. Deactivate an appointment slot.

### Backend Testing

Navigate to the backend directory and execute:

```bash
pytest -q
```

### Frontend Testing

Navigate to the frontend directory:

```bash
npm test
```

Build the frontend:

```bash
npm run build
```

## 📖 Swagger API Testing

FastAPI provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

To test protected endpoints:

1. Execute the login API.
2. Copy the generated `access_token`.
3. Click the Authorize button.
4. Enter the token.
5. Click Authorize.
6. Execute protected APIs.

Swagger allows testing authentication, appointment creation, booking, cancellation, and rescheduling.

## 🔒 Security Considerations

- Passwords are hashed using Argon2.
- JWT authentication protects private endpoints.
- Role-based authorization restricts admin operations.
- Environment variables store sensitive configuration.
- `.env` files should never be committed to GitHub.
- Database credentials should not be exposed in frontend code.
- Production deployment should use HTTPS, secure cookie handling, CSRF protection, and rate limiting.

## 🌟 Future Enhancements

- Email and SMS appointment notifications.
- Payment gateway integration.
- Doctor and service provider management.
- Appointment search and filtering.
- Calendar integration.
- Appointment reminders.
- Admin analytics dashboard.
- Docker-based deployment.
- Cloud hosting and CI/CD integration.

## 👨‍💻 Author

**Sai Harshith Bachina**

GitHub: https://github.com/saiharshith123

LinkedIn: https://www.linkedin.com/in/bachina-sai-harshith-b06a50208/

## 📄 License

This project is developed for learning, demonstration, and portfolio purposes.
