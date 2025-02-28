from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interactions

DATABASE = "inventory.db"

# Function to Connect to SQLite Database
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return dictionary-like row results
    return conn

# Create Products Table (Run Once)
def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                expiry_date TEXT,
                supplier TEXT
            )
        ''')
        conn.commit()

# ---------------- CRUD API Routes ----------------

# Get All Products
@app.route("/products", methods=["GET"])
def get_products():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = [dict(row) for row in cursor.fetchall()]
    return jsonify(products)

# Get a Single Product by ID
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
    return jsonify(dict(product)) if product else jsonify({"error": "Product not found"}), 404

# Add a New Product
@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, category, quantity, price, expiry_date, supplier) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data["name"], data["category"], data["quantity"], data["price"], data.get("expiry_date"), data["supplier"]))
        conn.commit()
        new_id = cursor.lastrowid
    return jsonify({"message": "Product added", "id": new_id}), 201

# Update an Existing Product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products 
            SET name=?, category=?, quantity=?, price=?, expiry_date=?, supplier=? 
            WHERE id=?
        ''', (data["name"], data["category"], data["quantity"], data["price"], data.get("expiry_date"), data["supplier"], product_id))
        conn.commit()
    return jsonify({"message": "Product updated"})

# Delete a Product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
    return jsonify({"message": "Product deleted"})


# Run the Flask App
if __name__ == "__main__":
    create_table()  # Ensure table exists before running
    app.run(debug=True)
