import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Choose another.", "danger")
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. You can log in now.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid username or password.", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    stock_items = Stock.query.all()
    return render_template('index.html', stock_items=stock_items)

@app.route('/add', methods=['POST'])
@login_required
def add_stock():
    name = request.form['name']
    quantity = request.form['quantity']
    price = request.form['price']
    if not name or not quantity or not price:
        flash("All fields are required!", "danger")
        return redirect(url_for('index'))
    new_item = Stock(name=name, quantity=int(quantity), price=float(price))
    db.session.add(new_item)
    db.session.commit()
    flash("Stock item added successfully.", "success")
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_stock(id):
    item = Stock.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = int(request.form['quantity'])
        item.price = float(request.form['price'])
        db.session.commit()
        flash("Stock item updated successfully.", "success")
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_stock(id):
    item = Stock.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(item)
        db.session.commit()
        flash("Stock item deleted successfully.", "success")
        return redirect(url_for('index'))
    return render_template('delete.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)

