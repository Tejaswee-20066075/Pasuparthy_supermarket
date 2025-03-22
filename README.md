# Supermarket Inventory Management System

## Overview
This project is a simple web-based inventory management system for a supermarket. It allows administrators to add, edit, view, and delete products using a Flask backend with an SQLite database and a JavaScript-powered frontend.


## Features
- View all products in inventory
- Add new products
- Edit existing products
- Delete products
- Persist data using SQLite

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask, SQLite
- **API Communication:** Fetch API

## Installation and Setup

### Prerequisites
Make sure you have Python installed on your system. You can check by running:
```bash
python --version
```

### Steps to Run the Project
1. **Clone the repository:**
```bash
git clone https://github.com/your-repo-link.git
cd supermarket-inventory
```

2. **Set up a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r backend/requirements.txt
```

4. **Run the Flask server:**
```bash
python app.py
```
This will start the API at `http://127.0.0.1:5000`

5. **Open the frontend in a browser:**
Simply open `frontend/index.html` in your browser.

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/products` | Retrieve all products |
| GET | `/products/{id}` | Retrieve a specific product |
| POST | `/products` | Add a new product |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |
