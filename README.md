Library Management System API
Django
DRF
PostgreSQL
Heroku

A RESTful API for managing library operations including book checkouts, returns, and inventory management.

Features
Books Management: CRUD operations for library books

User Management: CRUD operations for library users

Authentication: Token-based authentication for secure access

Book Transactions: Checkout and return books with automatic inventory updates

Filtering: Search books by title, author, ISBN, or availability

User History: View individual user transaction history

API Endpoints
Endpoint	Method	Description	Authentication Required
/api/auth/	POST	Obtain authentication token	No
/api/users/	GET, POST	List all users or create new user	Admin only
/api/users/<id>/	GET, PUT, DELETE	Retrieve, update or delete user	Admin only
/api/books/	GET, POST	List all books or add new book	GET: No, POST: Yes
/api/books/<id>/	GET, PUT, DELETE	Retrieve, update or delete book	GET: No, Others: Yes
/api/checkout/	POST	Checkout a book	Yes
/api/return/<id>/	PUT	Return a checked out book	Yes
/api/my-transactions/	GET	View user's transaction history	Yes
Setup Instructions
Prerequisites
Python 3.9+

PostgreSQL (for production)

Git

Local Development
Clone the repository

bash
Copy
git clone https://github.com/yourusername/library-management-api.git
cd library-management-api
Set up virtual environment

bash
Copy
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
pip install -r requirements.txt
Configure database

For development, SQLite is configured by default

For production, update DATABASES in backend/backend/settings.py

Run migrations

bash
Copy
python manage.py migrate
Create superuser

bash
Copy
python manage.py createsuperuser
Run development server

bash
Copy
python manage.py runserver
Deployment to Heroku
Install Heroku CLI and login

bash
Copy
heroku login
Create Heroku app

bash
Copy
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
Deploy to Heroku

bash
Copy
git push heroku main
Run migrations

bash
Copy
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
Collect static files

bash
Copy
heroku run python manage.py collectstatic
API Documentation
After running the server, access the interactive API documentation at:

http://localhost:8000/docs/ (development)
or
https://your-app-name.herokuapp.com/docs/ (production)

Example Requests
Get Authentication Token
bash
Copy
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "password":"password123"}' http://localhost:8000/api/auth/
List All Books
bash
Copy
curl -H "Authorization: Token yourtoken" http://localhost:8000/api/books/
Checkout a Book
bash
Copy
curl -X POST -H "Authorization: Token yourtoken" -H "Content-Type: application/json" -d '{"book":1}' http://localhost:8000/api/checkout/
Return a Book
bash
Copy
curl -X PUT -H "Authorization: Token yourtoken" http://localhost:8000/api/return/1/
Models
Book
title: CharField (required)

author: CharField (required)

isbn: CharField (required, unique)

published_date: DateField (required)

copies_available: PositiveIntegerField (default=1)

User
Extends Django's AbstractUser with:

email: EmailField (unique)

date_joined: DateField (auto_now_add)

is_active: BooleanField (default=True)

Transaction
user: ForeignKey to User

book: ForeignKey to Book

checkout_date: DateTimeField (auto_now_add)

return_date: DateTimeField (nullable)

is_returned: BooleanField (default=False)

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Django REST Framework for the powerful API toolkit

Heroku for the deployment platform

The Django community for excellent documentation and suppor
