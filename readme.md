# Country Info App

A comprehensive Django application that provides detailed information about countries using PostgreSQL as the database backend.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- PostgreSQL
- Git

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Rafin298/country_info_app.git
cd country_info_app
```

### 2. Set up a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory with the following variables:

```
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
```

> **Note:** Make sure to replace the placeholders with your actual database credentials.

### 5. Set up the PostgreSQL database

Create a PostgreSQL database using the credentials specified in your `.env` file.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

## 🚀 Running the Project

Start the development server:

```bash
python manage.py runserver
```

The application will be available at [http://localhost:8000/](http://localhost:8000/).

## 📥 Data Import

The application includes a management command to fetch country data from the [REST Countries API](https://restcountries.com/):

### Import all country data

```bash
python manage.py fetch_countries
```

### Reset and import all country data

This will delete all existing country data before importing:

```bash
python manage.py fetch_countries --reset
```

## 🌐 Live Demo

The application is available online at: [https://country-info-app-seven.vercel.app/](https://country-info-app-seven.vercel.app/)

You can register for a new account or use these guest credentials to login:
- Username: guest
- Password: Abcd123#

## 📝 Features

- Country information database
- Backend development with Django
- Creating RESTful APIs
- Frontend development with HTML, CSS, and JavaScript
- Data presentation and user interface design
- User authentication
## 👨‍💻 Author

[Rafin298](https://github.com/Rafin298)
