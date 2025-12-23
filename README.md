# 🏥 MediCare - Hospital Management System

A comprehensive Django-based hospital appointment management system that enables patients to book appointments with doctors and allows doctors to manage their availability schedules.

---

## 🚀 Features

- **Patient Management**: Register, manage profiles, and book appointments
- **Doctor Management**: Admin can add doctors with specializations
- **Appointment Booking**: Patients can book available time slots with doctors
- **Doctor Availability**: Doctors can set their available days and times
- **Admin Dashboard**: Comprehensive dashboard for managing the entire system
- **Responsive Design**: Modern UI that works on all devices

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2.9
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/omar52478/MediCare.git
cd MediCare
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
```

#### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Apply Migrations
```bash
python manage.py migrate
```

#### 6. Create Admin Account
```bash
python manage.py createsuperuser
```

#### 7. Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

---

## 🔐 User Roles

| Role | Creation Method | Permissions |
|------|-----------------|-------------|
| **Admin** | `python manage.py createsuperuser` | Full access, manage doctors & patients |
| **Doctor** | Added via Admin Dashboard | Manage availability, view appointments |
| **Patient** | Self-registration at `/accounts/signup/` | Book appointments, view bookings |

---

## 🔗 Available Routes

### Public Pages
| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/accounts/signup/` | Patient registration |
| `/accounts/login/` | User login |
| `/accounts/about/` | About page |

### User Pages
| Route | Description |
|-------|-------------|
| `/accounts/profile/` | User profile |
| `/accounts/book/` | Book appointment (Patients) |
| `/accounts/my_availability/` | Manage availability (Doctors) |

### Admin Pages
| Route | Description |
|-------|-------------|
| `/admin/` | Django Admin Panel |
| `/accounts/dashboard/` | Custom Admin Dashboard |
| `/accounts/dashboard/patients/` | Manage Patients |
| `/accounts/dashboard/doctors/` | Manage Doctors |
| `/accounts/dashboard/appointments/` | Manage Appointments |
| `/accounts/dashboard/specializations/` | Manage Specializations |

---

## 📂 Project Structure

```
MediCare/
├── accounts/                 # Main application
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   ├── admin/          # Admin dashboard templates
│   │   └── *.html          # Main templates
│   ├── static/              # CSS & JavaScript files
│   ├── models.py            # Data models
│   ├── views.py             # View functions
│   └── urls.py              # URL routing
├── project/                  # Project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL configuration
├── media/                    # User uploaded files
├── requirements.txt          # Python dependencies
├── Procfile                  # Render deployment
├── build.sh                  # Build script
└── README.md                 # This file
```

---

## 📊 Data Models

| Model | Description |
|-------|-------------|
| **Profile** | Patient information (phone, age, address, emergency contact) |
| **Doctor** | Doctor linked to user with specialization |
| **Specialization** | Medical specializations |
| **DoctorAvailability** | Doctor's available days and times |
| **Appointment** | Booked appointments between patients and doctors |

---

## 🚀 Deployment

This project is configured for deployment on Render. See `DEPLOYMENT.md` for detailed instructions.

### Quick Deploy
1. Push to GitHub
2. Connect repository to Render
3. Set environment variables:
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: `False`
   - `DATABASE_URL`: PostgreSQL connection string

---

## 🛠️ Useful Commands

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files (production)
python manage.py collectstatic
```

---

## ⚠️ Production Notes

1. Set `DEBUG = False` in production
2. Use a secure `SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Configure `ALLOWED_HOSTS` properly
5. Enable HTTPS

---

## � License

This project is for educational purposes.

---

## 👨‍� Author

Hospital Management System - MediCare
