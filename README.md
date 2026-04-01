TODO PROJECT (Django REST API)
A simple ToDo application built using Django and Django REST Framework (DRF).
This project allows users to create, view, update, and delete tasks via REST APIs.

**Features**
1. Create new tasks
2. View all tasks
3. Retrieve single task details
4. Update tasks (full & partial update)
5. Delete tasks

**RESTful API design using Django REST Framework**

Tech Stack
Python
Django
Django REST Framework
SQLite (default database)
Postman (for API testing)

📁 Project Structure
ToDo-Project/
│
├── tasks/               # Main app
│   ├── models.py        # Task model
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # App routes
│
├── project/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

**Installation & Setup**

1️. Clone the repository
git clone https://github.com/sumithras21/ToDo-Project.git
cd ToDo-Project

2️. Create virtual environment
python -m venv venv

Activate:  Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate
3️. Install dependencies pip install -r requirements.txt
4️. Run migrations
    python manage.py makemigrations
    python manage.py migrate

5️. Create superuser (optional):  python manage.py createsuperuser
6️: Run server  python manage.py runserver

API Endpoints
Method	  Endpoint	        Description
GET	    /api/tasks/	        Get all tasks
POST	  /api/tasks/	        Create new task
GET	    /api/tasks/{id}/	  Get single task
PUT	    /api/tasks/{id}/	  Update task
PATCH	   /api/tasks/{id}/	  Partial update
DELETE	/api/tasks/{id}/	  Delete task

Example JSON (POST request)
{
  "title": "Complete Django Project",
  "description": "Finish REST API and testing"
}

Testing with Postman
Open Postman: Use http://127.0.0.1:8000/api/tasks/
Select method (GET, POST, PUT, DELETE)
Send request and view response

Common Issues
1. No Tasks matches the given query
2. Task ID does not exist
3. Create a task first using POST
