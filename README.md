# Django Task Management API

This project is a Django-based Task Management API that allows users to manage tasks and categories. It provides endpoints for user registration, login, creating, updating, and deleting tasks and categories. Authentication is handled using token-based authentication.

## Features
- User registration and login
- Token-based authentication
- CRUD operations for tasks
- CRUD operations for categories
- Task filtering by user
- Custom error handling and response messages

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django 4.x
- Django Rest Framework (DRF)
- PostgreSQL or any other supported database
- Postman (for API testing, optional)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mehens1/task_management_system_api.git
    cd django-task-management-api
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    Update the `DATABASES` settings in `settings.py` with your database credentials.

    Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:
    ```bash
    python manage.py runserver 8080
    ```

### API Endpoints

| **Route**                   | **Method** | **Description**                  | **Authentication**   |
|-----------------------------|------------|----------------------------------|----------------------|
| `/register`                 | POST       | Register a new user              | Public               |
| `/login`                    | POST       | Log in and retrieve token        | Public               |
| `/tasks`                    | GET        | Get list of tasks                | Token required       |
| `/task/create`              | POST       | Create a new task                | Token required       |
| `/task/<int:pk>/update`     | PUT/PATCH  | Update an existing task          | Token required       |
| `/task/<int:pk>/delete`     | DELETE     | Delete a task                    | Token required       |
| `/categories`               | GET        | Get list of categories           | Token required       |
| `/category/create`          | POST       | Create a new category            | Token required       |
| `/category/<int:pk>/update` | PUT/PATCH  | Update an existing category      | Token required       |
| `/category/<int:pk>/delete` | DELETE     | Delete a category                | Token required       |

### Authentication
The API uses token-based authentication. To access protected routes, you need to include the token in the Authorization header as a Bearer token.

Example:
```bash
Authorization: Token <your-token>
