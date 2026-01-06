# 📝 Django To-Do Application with User Management System

A full-featured **Django To-Do Application** with **authentication, user-specific tasks, and a custom admin dashboard** for managing users.  
This project is built using **Django best practices** with a clean UI and secure access control.

---

## 🚀 Features

### 👤 User Features
- User registration & login
- Secure authentication system
- Create, update, delete tasks
- Mark tasks as completed
- Each user sees **only their own tasks**
- Search tasks
- Logout functionality

---

### 🛠️ Admin Features (Custom Admin Dashboard)
- Separate admin login
- View all registered users
- Search users by username or email
- Pagination with continuous numbering
- Register new users
- Edit user details
- Activate / deactivate users (with confirmation)
- Prevent admin & superuser modification
- Styled admin interface (not Django default admin)

---

### 🔐 Security & Best Practices
- CSRF protection
- POST-only actions for destructive operations
- Login & permission checks
- Admin-only protected views
- Email uniqueness validation
- Password confirmation validation
- Cache control using `@never_cache`

---

## 🧩 Tech Stack

- **Backend:** Django (Python)
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS
- **Authentication:** Django Auth System
- **Pagination:** Django Paginator
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

