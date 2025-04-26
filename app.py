import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import send_from_directory

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model for Admin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Stock Model
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Apply database migrations
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists.'}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration successful.'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful.'})
    return jsonify({'error': 'Invalid credentials.'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully.'})

@app.route('/api/stock', methods=['GET'])
@login_required
def get_stock():
    stock_items = Stock.query.all()
    result = [
        {'id': item.id, 'name': item.name, 'quantity': item.quantity, 'price': item.price}
        for item in stock_items
    ]
    return jsonify(result)

@app.route('/api/stock', methods=['POST'])
@login_required
def add_stock():
    data = request.json
    name = data.get('name')
    quantity = data.get('quantity')
    price = data.get('price')
    if not name or quantity is None or price is None:
        return jsonify({'error': 'Missing fields'}), 400
    new_item = Stock(name=name, quantity=quantity, price=price)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Stock item added successfully.'}), 201

@app.route('/api/stock/<int:id>', methods=['PUT'])
@login_required
def update_stock(id):
    item = Stock.query.get_or_404(id)
    data = request.json
    item.name = data.get('name', item.name)
    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify({'message': 'Stock item updated successfully.'})

@app.route('/api/stock/<int:id>', methods=['DELETE'])
@login_required
def delete_stock(id):
    item = Stock.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Stock item deleted successfully.'})

@app.route('/index.html')
def serve_home():
    return send_from_directory('templates', 'index.html')

@app.route('/')
def serve_login():
    return send_from_directory('templates', 'login.html')

@app.route('/register.html')
def serve_register():
    return send_from_directory('templates', 'register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
