

# Flask Catalog API

A RESTful API built with Flask for managing products and users in an catalog database. This API provides endpoints for product management, user authentication, and product search functionality.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Dark Mode Support](#dark-mode-support)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Product Management**: Create and retrieve product information
- **User Authentication**: Register and login functionality
- **Search Capability**: Search products by name or description
- **Database Integration**: SQLAlchemy ORM for database operations
- **CORS Support**: Cross-Origin Resource Sharing enabled
- **Environment Configuration**: Secure configuration using environment variables

## Technologies Used

- **Flask**: Lightweight web framework for Python
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping
- **Flask-CORS**: Extension for handling Cross-Origin Resource Sharing
- **python-dotenv**: Loading environment variables from .env files
- **SQLite**: Database (configurable to other databases)

## Project Structure

```
flask-ecommerce-api/
├── app.py                  # Main application file with routes and models
├── init_db.py              # Database initialization script
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── instance/               # Instance-specific data (including SQLite database)
└── static/                 # Static files (CSS, JS, images)
    └── css/
        └── main.css        # Main stylesheet with dark mode support
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd flask-ecommerce-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install flask flask-cors flask-sqlalchemy python-dotenv
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=sqlite:///instance/ecommerce.db
FLASK_APP=app.py
FLASK_ENV=development
```

You can modify the `DATABASE_URL` to use other database systems like PostgreSQL or MySQL.

## Database Setup

Initialize the database by running:

```bash
python init_db.py
```

This will create all the necessary tables defined in the models.

## API Endpoints

### Products

- **GET /products**
  - Description: Retrieve all products
  - Response: List of product objects

- **POST /products**
  - Description: Add a new product
  - Request Body: JSON with product details (name, description, price, quantity)
  - Response: Success message

### Users

- **POST /users**
  - Description: Add a new user
  - Request Body: JSON with user details (username, password, email)
  - Response: Success message

### Authentication

- **POST /auth/login**
  - Description: User login
  - Request Body: JSON with credentials (username, password)
  - Response: Success message and username

- **POST /auth/register**
  - Description: User registration
  - Request Body: JSON with user details (username, password, email)
  - Response: Success message

### Search

- **POST /search**
  - Description: Search for products
  - Request Body: JSON with search_query
  - Response: List of matching products

## Usage Examples

### Adding a Product

```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smartphone",
    "description": "Latest model smartphone with advanced features",
    "price": 799.99,
    "quantity": 50
  }'
```

### User Registration

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user123",
    "password": "securepassword",
    "email": "user@example.com"
  }'
```

### Searching Products

```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "smartphone"
  }'
```

## Dark Mode Support

The application includes CSS that supports both light and dark modes based on user system preferences using the `prefers-color-scheme` media query. The color scheme automatically adjusts to match the user's system settings.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Security Considerations

Note that this implementation stores passwords in plain text, which is not secure for production environments. For a production application, consider implementing password hashing using libraries like `bcrypt` or `passlib`.

## Future Improvements

- Add password hashing for user security
- Implement JWT authentication
- Add product categories and filtering
- Create admin dashboard functionality
- Add unit and integration tests
