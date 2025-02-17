from flask import Flask, render_template, request, session, redirect, flash, url_for
import sqlite3
from contextlib import closing
import os

# Get the absolute path to the folder
basedir = os.path.abspath(os.path.dirname(_file_))

# Specify the absolute path to the database file
DATABASE = os.path.join(basedir, 'mydatabase.db')

app = Flask(_name_)

# Secret key for session management
app.secret_key = os.urandom(24)

# SQLite setup
def get_db_connection():
    conn = sqlite3.connect(DATABASE)  # Changed to mydatabase.db
    conn.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return conn

# Home/Registration page
@app.route('/')
def index():
    return render_template('register.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']

    # Insert user data into the database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email))
    conn.commit()
    conn.close()

    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['username']  # Store user session
            flash('Login successful!', 'success')
            return redirect(url_for('profile', username=user['username']))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

# Profile page (show user details)
@app.route('/profile/<username>')
def profile(username):
    if 'user_id' not in session or session['user_id'] != username:
        flash('You must log in to view your profile.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    return render_template('profile.html', user=user)

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if _name_ == '_main_':
    app.run(debug=True)
