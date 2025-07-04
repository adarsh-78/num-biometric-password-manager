from flask import Flask
import sqlite3

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db():
    conn = sqlite3.connect("passwords.db")
    return conn

# Home route
@app.route('/')
def home():
    return "Flask with SQLite is working!"

# Route to insert a sample user
@app.route('/add-user')
def add_user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        ("Test User", "test@example.com", "testpassword123")
    )
    db.commit()
    return "User inserted successfully!"

# Route to display all users
@app.route('/users')
def show_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    output = ""
    for user in users:
        output += f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Password: {user[3]}<br>"

    return output

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
