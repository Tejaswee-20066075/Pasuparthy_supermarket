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


# Run the Flask App
if __name__ == "__main__":
    create_table()  # Ensure table exists before running
    app.run(debug=True)
