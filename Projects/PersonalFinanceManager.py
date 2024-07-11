from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from cerberus import Validator
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import logging

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or 'jwt_secret_key'

# Extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
jwt = JWTManager(app)

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    expenses = db.relationship('Expense', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/add_expense', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    validator = Validator({
        'category': {'type': 'string', 'required': True},
        'amount': {'type': 'float', 'required': True},
        'date': {'type': 'datetime', 'required': True}
    })
    if not validator.validate(data):
        return jsonify({'error': 'Invalid data', 'errors': validator.errors}), 400
    
    expense = Expense(category=data['category'], amount=data['amount'], date=data['date'], author=current_user)
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'}), 201

@app.route('/get_expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    expenses_data = [{'category': e.category, 'amount': e.amount, 'date': e.date} for e in expenses]
    return jsonify(expenses_data), 200

@app.route('/set_budget', methods=['POST'])
@jwt_required()
def set_budget():
    data = request.get_json()
    # Add budget setting logic here
    return jsonify({'message': 'Budget set successfully'}), 201

@app.route('/generate_report', methods=['GET'])
@jwt_required()
def generate_report():
    # Add report generation logic here
    return jsonify({'message': 'Report generated successfully'}), 200

# Error handlers
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return jsonify({'error': 'Unauthorized access'}), 401

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

# Explanation
# Configuration: The app is configured with a secret key and SQLAlchemy database URI.
# Models: Two models, User and Expense, are defined using SQLAlchemy.
# Routes:
# User Registration: /register endpoint for user registration.
# User Login: /login endpoint for user login.
# User Logout: /logout endpoint for user logout.
# Add Expense: /add_expense endpoint for adding an expense.
# Get Expenses: /get_expenses endpoint for retrieving all expenses of the logged-in user.
# Set Budget: /set_budget endpoint for setting a budget (logic not implemented).
# Generate Report: /generate_report endpoint for generating a financial report (logic not implemented).
# Extensions: Flask extensions such as Flask-Login, Flask-SQLAlchemy, and Flask-Migrate are used.
# User Authentication: User authentication is managed with Flask-Login.
# Run the App: The app runs in debug mode when executed directly.
# Running the App
# Install the dependencies:
# bash
# Copy code
# pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login
# Create the database and apply migrations:
# bash
# Copy code
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade
# Run the Flask app:
# bash
# Copy code
# python your_file_name.py
# Replace your_file_name.py with the actual filename where you saved the script. The Flask app will be accessible at http://127.0.0.1:5000/. Use tools like Postman or cURL to interact with the API endpoints.