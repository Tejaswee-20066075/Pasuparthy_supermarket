from flask import Flask, request, jsonify, render_template, g
from flask_cors import CORS
import sqlite3
import os

# Initialize Flask App
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for frontend interactions

DATABASE = "inventory.db"

# Function to Connect to SQLite Database
def get_db():
    """ Connect to the database and reuse the connection for performance. """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return dictionary-like row results
    return g.db

@app.teardown_appcontext
def close_db(error):
    """ Close database connection at the end of each request. """
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Create Products Table (Run Once)
def create_table():
    with sqlite3.connect(DATABASE) as conn:
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

# ---------------- Frontend Routes ----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add_page():
    return render_template("add.html")

@app.route("/edit")
def edit_page():
    return render_template("edit.html")

@app.route("/delete")
def delete_page():
    return render_template("delete.html")

# ---------------- CRUD API Routes ----------------

@app.route("/products", methods=["GET"])
def get_products():
    """ Get all products from the database. """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        products = [dict(row) for row in cursor.fetchall()]
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": "Failed to retrieve products", "details": str(e)}), 500

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """ Get a single product by ID. """
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        return jsonify(dict(product)) if product else jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to retrieve product", "details": str(e)}), 500

@app.route("/products", methods=["POST"])
def add_product():
    """ Add a new product to the database. """
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO products (name, category, quantity, price, expiry_date, supplier) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data["name"], data["category"], data["quantity"], data["price"], data.get("expiry_date"), data["supplier"]))
        db.commit()
        new_id = cursor.lastrowid
        return jsonify({"message": "Product added successfully", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": "Failed to add product", "details": str(e)}), 500

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """ Update an existing product. """
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            UPDATE products 
            SET name=?, category=?, quantity=?, price=?, expiry_date=?, supplier=? 
            WHERE id=?
        ''', (data["name"], data["category"], data["quantity"], data["price"], data.get("expiry_date"), data["supplier"], product_id))
        db.commit()
        return jsonify({"message": "Product updated successfully"})
    except Exception as e:
        return jsonify({"error": "Failed to update product", "details": str(e)}), 500

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """ Delete a product by ID with better error handling. """
    try:
        db = get_db()
        cursor = db.cursor()

        # Check if product exists
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            return jsonify({"error": f"Product ID {product_id} not found"}), 404

        # Perform deletion
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        db.commit()
        return jsonify({"message": f"Product ID {product_id} deleted successfully"})
    except Exception as e:
        return jsonify({"error": "Failed to delete product", "details": str(e)}), 500

# ---------------- Health Check Route ----------------
@app.route("/health", methods=["GET"])
def health_check():
    """ Simple health check route to confirm API is running. """
    return jsonify({"status": "OK", "message": "API is running"}), 200

# ---------------- Run the Flask App ----------------
if __name__ == "__main__":
    create_table()  # Ensure table exists before running
    app.run(debug=True)


