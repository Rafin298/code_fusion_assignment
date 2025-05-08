Django Project
A comprehensive Django application using PostgreSQL as the database backend.
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+
PostgreSQL
Git

Installation
1. Clone the repository
bash:
git clone https://github.com/Rafin298/country_info_app.git
cd country_info_app

2. Set up a virtual environment
bash:
python -m venv venv
Activate the virtual environment:
On Windows:
venv\Scripts\activate
On macOS/Linux:
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables
Create a .env file in the project root directory with the following variables:

DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
Note: Make sure to replace the placeholders with your actual database credentials.
5. Set up the PostgreSQL database

Create a PostgreSQL database using the credentials specified in your .env file.

6. Apply migrations
python manage.py migrate
7. Create a superuser (optional)
python manage.py createsuperuser
Running the Project
Start the development server:
bashpython manage.py runserver
The application will be available at http://localhost:8000/.
