from app import app
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
import re

from app.encryption_helper import encrypt_password, decrypt_password


def get_db():
    return sqlite3.connect("passwords.db")


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


@app.route('/')
def home():
    return redirect(url_for("login"))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if not is_valid_email(email):
            flash("Invalid email format.", "error")
            return redirect(url_for("register"))

        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Email is already registered.", "error")
            db.close()
            return redirect(url_for("register"))

        encrypted_password = encrypt_password(password)
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, encrypted_password))
        db.commit()
        db.close()

        flash("Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_input = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        db.close()

        if user:
            try:
                stored_encrypted_password = user[3]
                decrypted_password = decrypt_password(stored_encrypted_password)

                if password_input == decrypted_password:
                    session["user_id"] = user[0]
                    session["user_name"] = user[1]
                    return redirect(url_for("dashboard"))
                else:
                    flash("Incorrect password.", "error")
            except:
                flash("Decryption error.", "error")
        else:
            flash("User not found.", "error")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        flash("Please login first.", "error")
        return redirect(url_for("login"))

    return render_template("dashboard.html", user_name=session["user_name"])


@app.route('/save-password', methods=["GET", "POST"])
def save_password():
    if "user_id" not in session:
        flash("Login required to save passwords.", "error")
        return redirect(url_for("login"))

    if request.method == 'POST':
        site = request.form['site']
        site_username = request.form['site_username']
        site_password = encrypt_password(request.form['site_password'])

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO credentials (user_id, site_name, site_username, site_password)
            VALUES (?, ?, ?, ?)
        """, (session["user_id"], site, site_username, site_password))
        db.commit()
        db.close()

        flash("Password saved successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('save_password.html')


@app.route('/view-passwords')
def view_passwords():
    if "user_id" not in session:
        flash("Login required to view passwords.", "error")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, site_name, site_username, site_password FROM credentials WHERE user_id = ?", (session["user_id"],))
    records = cursor.fetchall()
    db.close()

    decrypted_data = []
    for cred_id, site, username, encrypted_password in records:
        try:
            decrypted_password = decrypt_password(encrypted_password)
        except:
            decrypted_password = "Decryption Failed"
        decrypted_data.append((cred_id, site, username, decrypted_password))

    return render_template("view_passwords.html", passwords=decrypted_data)


@app.route('/edit-password/<int:cred_id>', methods=["GET", "POST"])
def edit_password(cred_id):
    if "user_id" not in session:
        flash("Login required.", "error")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        site = request.form["site"]
        username = request.form["site_username"]
        password = encrypt_password(request.form["site_password"])

        cursor.execute("""
            UPDATE credentials
            SET site_name = ?, site_username = ?, site_password = ?
            WHERE id = ? AND user_id = ?
        """, (site, username, password, cred_id, session["user_id"]))
        db.commit()
        db.close()

        flash("Password updated successfully!", "success")
        return redirect(url_for("view_passwords"))

    cursor.execute("""
        SELECT site_name, site_username, site_password
        FROM credentials
        WHERE id = ? AND user_id = ?
    """, (cred_id, session["user_id"]))
    record = cursor.fetchone()
    db.close()

    if record:
        try:
            decrypted_password = decrypt_password(record[2])
        except:
            decrypted_password = "Decryption Failed"
        return render_template("edit_password.html", cred_id=cred_id, site=record[0], username=record[1], password=decrypted_password)
    else:
        flash("Record not found.", "error")
        return redirect(url_for("view_passwords"))


@app.route('/delete-password/<int:cred_id>')
def delete_password(cred_id):
    if "user_id" not in session:
        flash("Login required.", "error")
        return redirect(url_for("login"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM credentials WHERE id = ? AND user_id = ?", (cred_id, session["user_id"]))
    db.commit()
    db.close()

    flash("Password deleted successfully!", "success")
    return redirect(url_for("view_passwords"))


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))
