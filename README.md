# FastAPI Authentication API

A simple authentication REST API built with **Python and FastAPI**. It allows users to register, log in, view their profile, update their information, and delete their account.

I built this project to practice backend development and understand how authentication works in a real application. While working on it, I got hands-on experience with databases, password hashing, JWT tokens, protected routes, and API testing.

## Features

- **User Registration** — Create an account with a username, email, and password.
- **User Login** — Authenticate using a username and password and receive a JWT access token.
- **Password Hashing** — Store hashed passwords using bcrypt instead of plain-text passwords.
- **Protected Routes** — Restrict profile-related operations to authenticated users.
- **Profile Management** — View and update account information.
- **Account Deletion** — Allow authenticated users to delete their accounts.
- **Error Handling** — Handle duplicate usernames, duplicate emails, invalid credentials, and unauthorized requests.
- **API Documentation** — Explore and test endpoints using FastAPI's Swagger UI.

## Tech Stack

- **Python** — Backend programming language
- **FastAPI** — REST API framework
- **SQLAlchemy** — Database ORM
- **PostgreSQL** — Relational database
- **Pydantic** — Request and response validation
- **JWT** — Token-based authentication
- **Passlib & bcrypt** — Password hashing
- **Pytest** — API testing

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate and receive an access token |
| GET | `/me` | Get the current user's profile |
| PATCH | `/update` | Update account information |
| DELETE | `/delete` | Delete the authenticated user's account |

The profile, update, and delete endpoints require a valid bearer token.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/talhaahmad56/fastapi-authentication-api.git
cd fastapi-authentication-api
```

### 2. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=replace_with_a_long_random_secret_key
ALGORITHM=HS256
```

Replace the placeholder values with your own configuration. Make sure the PostgreSQL database exists before starting the application.

Never commit your actual `.env` file or credentials to GitHub.

### 5. Run the application

```bash
uvicorn main:app --reload
```

Once the server starts, open:

**http://127.0.0.1:8000/docs**

You can use Swagger UI to explore the API and test its endpoints.

## Testing

The project includes API tests using Pytest.

To run the tests:

```bash
pytest -v
```

## What I Learned

This project helped me understand how different parts of a backend application work together.

Some of the main things I practiced were:

- Connecting FastAPI with a relational database using SQLAlchemy.
- Creating and validating request and response schemas with Pydantic.
- Hashing passwords and verifying user credentials.
- Generating and validating JWT access tokens.
- Protecting endpoints using FastAPI dependencies.
- Handling common API errors with appropriate HTTP status codes.
- Organizing backend code into separate modules.
- Writing and running API tests.

One of my biggest takeaways was understanding that authentication involves more than checking a username and password. It also requires careful handling of credentials, tokens, database records, and access to protected resources.

## Future Improvements

There are still features I'd like to add as I continue learning backend development:

- Refresh tokens and logout support
- Email verification
- Password reset functionality
- Rate limiting for authentication endpoints
- Database migrations using Alembic
- Deployment to a cloud platform

## About This Project

This is a personal learning project and part of my journey toward becoming a Python backend developer.

My goal was to build something practical, strengthen my understanding of FastAPI, and get more comfortable working with authentication and databases.

**Built by [Talha Ahmad](https://github.com/talhaahmad56)**
