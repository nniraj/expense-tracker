# 💰 Expense Tracker

A full-stack web application for tracking personal expenses with category management, JWT authentication, and comprehensive REST APIs.

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Development Guides](#-development-guides)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Authentication
- ✅ User Registration with email validation
- ✅ Secure Login with JWT token generation
- ✅ JWT-based Protected Routes
- ✅ Password hashing with bcrypt

### Expense Management
- ✅ Create, Read, Update, Delete expenses
- ✅ Track amount and description
- ✅ Optional category assignment
- ✅ Automatic timestamp tracking
- ✅ User-specific expense filtering

### Category Management
- ✅ Create expense categories
- ✅ View all categories
- ✅ Update category names
- ✅ Delete categories
- ✅ Shared across application

### Additional Features
- ✅ CORS enabled for frontend integration
- ✅ Comprehensive error handling
- ✅ Database migrations with Flask-Migrate
- ✅ Environment-based configuration
- ✅ Comprehensive API documentation

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 3.0.3
- **ORM:** SQLAlchemy 2.0.49
- **Authentication:** Flask-JWT-Extended 4.6.0
- **Database:** PostgreSQL
- **Migrations:** Flask-Migrate 4.0.7 (Alembic)
- **Password Hashing:** bcrypt
- **CORS:** Flask-CORS 4.0.1

### Frontend
- **Framework:** Angular
- **Language:** TypeScript
- **Build Tool:** Angular CLI

### Database
- **System:** PostgreSQL
- **Tables:** users, categories, expense
- **Relationships:** Foreign keys for data integrity

---

## 📁 Project Structure

```
expense_tracker/
├── backend/
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── user_models.py     # User model with auth methods
│   │   ├── expense_model.py   # Expense model
│   │   └── category_model.py  # Category model
│   ├── routes/                # API endpoints
│   │   ├── __init__.py
│   │   ├── auth_routes.py     # Register, Login
│   │   ├── expense_routes.py  # CRUD for expenses
│   │   └── category_routes.py # CRUD for categories
│   ├── migrations/            # Database migrations (Alembic)
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── versions/
│   ├── app.py                 # Flask app factory
│   ├── config.py              # Configuration management
│   ├── extensions.py          # Flask extensions (db, jwt, migrate)
│   ├── run.py                 # Application entry point
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables (local only)
│   ├── .env.example           # Example env file
│   └── .gitignore            # Git ignore rules
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Angular app
│   │   ├── assets/
│   │   └── main.ts
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── README.md                 # This file
├── ENVIRONMENT_SETUP.md     # Environment setup guide
└── .gitignore              # Root git ignore
```

---

## 📋 Prerequisites

- **Python:** 3.8 or higher
- **PostgreSQL:** 12 or higher
- **Node.js:** 14+ (for frontend)
- **npm/yarn:** For dependency management

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/expense_tracker.git
cd expense_tracker
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv env
```

#### Activate Virtual Environment

**Windows:**
```bash
.\env\Scripts\activate
```

**macOS/Linux:**
```bash
source env/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Copy from example
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_tracker

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this-in-production

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=1
```

**Important:** Never commit `.env` to Git. It's in `.gitignore`.

See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for detailed setup instructions.

---

## ▶️ Running the Application

### Backend

```bash
cd backend
python run.py
```

The backend will start at `http://localhost:5000`

### Frontend

```bash
cd frontend
ng serve
```

The frontend will be available at `http://localhost:4200`

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Routes

#### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password"
}
```

**Response (201):**
```json
{
    "success": true,
    "message": "User registered successfully"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "secure_password"
}
```

**Response (200):**
```json
{
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

### Expense Routes

#### Create Expense
```bash
POST /api/expenses
Authorization: Bearer {token}
Content-Type: application/json

{
    "amount": 50.99,
    "description": "Lunch at restaurant",
    "category_id": 1
}
```

#### Get All Expenses
```bash
GET /api/expenses
Authorization: Bearer {token}
```

#### Update Expense
```bash
PUT /api/expenses/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "amount": 60.00,
    "description": "Updated expense",
    "category_id": 2
}
```

#### Delete Expense
```bash
DELETE /api/expenses/{id}
Authorization: Bearer {token}
```

### Category Routes

#### Create Category
```bash
POST /api/categories
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Food"
}
```

#### Get All Categories
```bash
GET /api/categories
Authorization: Bearer {token}
```

#### Update Category
```bash
PUT /api/categories/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Groceries"
}
```

#### Delete Category
```bash
DELETE /api/categories/{id}
Authorization: Bearer {token}
```

---

## 💾 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
```

### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
```

### Expense Table
```sql
CREATE TABLE expense (
    id SERIAL PRIMARY KEY,
    description VARCHAR(200) NOT NULL,
    amount FLOAT NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    user_id INTEGER REFERENCES users(id),
    date TIMESTAMP DEFAULT now()
);
```

---

## 📖 Development Guides

Comprehensive documentation for developing and extending this project:

### Backend Development
- **[Backend Setup & Environment Variables](./ENVIRONMENT_SETUP.md)** - Configure database and JWT secrets
- **[Backend Architecture](./backend/README.md)** - Flask app structure, blueprints, and models (if created)

### Frontend Development
- **[Frontend Development Plan](./FRONTEND_DEVELOPMENT_PLAN.md)** - Complete roadmap for Angular features
  - Angular integration setup
  - Expense management UI
  - Dashboard with charts
  - Filters and pagination
  - Monthly summaries
  
- **[Frontend Setup Guide](./FRONTEND_SETUP.md)** - Step-by-step installation and configuration
  - Dependency installation
  - Service and guard setup
  - Component templates
  - Development server commands

### Key Files to Review
```
backend/
├── app.py              # Flask application factory
├── config.py           # Configuration management
├── routes/             # API endpoints
└── models/             # Database models

frontend/
├── src/app/
│   ├── services/       # API communication services
│   ├── guards/         # Route protection
│   ├── interceptors/   # JWT token injection
│   └── models/         # TypeScript interfaces
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add docstrings to all functions and classes
- Write meaningful commit messages
- Update tests when adding new features
- Keep `.env` credentials secure

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 💬 Contact & Support

For questions, issues, or suggestions:

- **Email:** your-email@example.com
- **Issues:** [GitHub Issues](https://github.com/yourusername/expense_tracker/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/expense_tracker/discussions)

---

## 🎯 Roadmap

- [ ] Expense filtering and search
- [ ] Advanced analytics and charts
- [ ] Multi-currency support
- [ ] Budget tracking and alerts
- [ ] Export to CSV/PDF
- [ ] Mobile app (React Native)
- [ ] Dark mode
- [ ] Two-factor authentication

---

## 📄 Changelog

### Version 1.0.0 (Initial Release)
- ✅ User authentication with JWT
- ✅ Complete CRUD for expenses
- ✅ Category management
- ✅ Database migrations setup
- ✅ API documentation
- ✅ Environment configuration

---

**Made with ❤️ by Nitin Niraj**

├── frontend/
│   ├── src/
│   ├── package.json
│   └── angular.json
│
└── README.md

---

# ⚙️ Backend Setup

## 1️⃣ Create Virtual Environment

```bash
python -m venv env