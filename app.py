"""
This is the main file for the Flask application.
It contains the routes for the API endpoints.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define model for products
class Products(db.Model):
    """
    This is the model for the products table.
    It contains the fields for the product.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(120), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    
    def __repr__(self):
        return f"<Product {self.name}>"
    

class Users(db.Model):
    """
    This is the model for the users table.
    It contains the fields for the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    
    def __repr__(self):
        return f"<User {self.username}>"
    

# Define route for getting all products
@app.route('/products', methods=["GET"])
def get_products():
    """
    This is the route for getting all products.
    It returns a list of all products in the database.
    """
    try:
        products = Products.query.all()
        print(products)
        product_list = []
        
        for product in products:
            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "image": product.image,
                "date_created": product.date_created
            }
            product_list.append(product_data)
        
        return jsonify(product_list)
    except Exception as e:
        return jsonify({"message": "Error fetching products", "error": str(e)}), 500

@app.route('/products', methods=["POST"])
def add_product():
    """
    This is the route for adding a new product to the database.
    It takes a JSON object with the product details and adds it to the database.
    """
    try:
        data = request.json
        new_product = Products(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
            image="1735215100460_photo_5_2024-12-26_12-00-29.jpg"
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"})
    except Exception as e:
        return jsonify({"message": "Error adding product", "error": str(e)}), 500
    
    
@app.route('/users', methods=["POST"])
def add_user():
    """
    This is the route for adding a new user to the database.
    It takes a JSON object with the user details and adds it to the database.
    """
    try:
        data = request.json
        new_user = Users(
            username=data["username"],
            password=data["password"],
            email=data["email"]
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"message": "Error adding user", "error": str(e)}), 500


@app.route('/auth/login', methods=["POST"])
def login():
    """
    This is the route for logging in a user.
    It takes a JSON object with the user details and logs in the user.
    """
    try:
        data = request.json
        user = Users.query.filter_by(username=data["username"]).first()
        if user and user.password == data["password"]:
            return jsonify({"message": "Login successful", "user": user.username})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"message": "Error logging in", "error": str(e)}), 500


@app.route('/auth/register', methods=["POST"])
def register():
    """
    This is the route for registering a new user.
    It takes a JSON object with the user details and registers the user.
    """
    try:
        data = request.json
        new_user = Users(
            username=data["username"],
            password=data["password"],
            email=data["email"]
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"message": "Error registering user", "error": str(e)}), 500

@app.route('/search', methods=["POST"])
def search():
    """
    This is the route for searching for products.
    It takes a JSON object with the search query and returns a list of products that match the search query.
    """
    try:
        data = request.json
        search_query = data["search_query"]
        products = Products.query.filter(
            or_(
                Products.name.ilike(f"%{search_query}%"), 
                Products.description.ilike(f"%{search_query}%")
                )
            ).all()
        product_list = []
        for product in products:
            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "quantity": product.quantity,
                "image": product.image,
                "date_created": product.date_created
            }
            product_list.append(product_data)
        return jsonify(product_list)
    except Exception as e:
        return jsonify({"message": "Error searching products", "error": str(e)}), 500


if __name__ == "__main__":
    """
    This is the main function that runs the Flask application.
    It runs the application in debug mode.
    """
    app.run(debug=True)