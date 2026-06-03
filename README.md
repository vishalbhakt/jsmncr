# JSM Shiksha Academy ERP (V2 Production)

A modern, scalable, and secure School Management System (ERP) built with a modular architecture for high-performance delivery.

## 🚀 Technology Stack
- **Frontend**: Next.js 15 (App Router), Tailwind CSS 4, Zustand, Lucide Icons, Framer Motion.
- **Backend**: Django 5, Django REST Framework, SimpleJWT (Auth).
- **Database**: PostgreSQL (Normalized).
- **Infrastructure**: Vercel (Frontend) + Render/Railway (Backend & DB).

## 🏛️ Modular Architecture
The system is divided into domain-specific modules:
- `authentication`: Secure JWT flow with custom User models.
- `users`: Detailed profiles for Students, Teachers, and Parents.
- `academics`: Class (Course), Subject, and Section management.
- `activities`: Daily operations like Attendance, Assignments, and Notes.
- `communication`: Announcements, Events, and Notifications.
- `finance`: Fee management and Payment tracking.

## 🛡️ Security Features
- **Strict RBAC**: Role-Based Access Control ensuring data privacy.
- **API Isolation**: Endpoints are filtered dynamically based on the logged-in user's role.
- **Route Guards**: Frontend protection preventing unauthorized access to dashboards.
- **Admin Approval**: New registrations must be approved by an administrator.

## 🛠️ Local Development
1. **Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📋 Role Access Guide
- **ADMIN**: Global control. Manage users, academics, and finances.
- **TEACHER**: Academic driver. Mark attendance, upload assignments/notes for assigned subjects.
- **STUDENT**: Learning consumer. Access resources, view attendance and results.
- **PARENT**: Monitor. View children's performance and manage fees.

---
Built with excellence for JSM Shiksha Academy.
