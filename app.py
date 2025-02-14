from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration using environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # For securing session cookies
db = SQLAlchemy(app)

# Define the Reservation model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    check_in = db.Column(db.String(10), nullable=False)
    check_out = db.Column(db.String(10), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    ticket_number = db.Column(db.String(10), unique=True, nullable=False)

# Admin credentials from .env file
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

# Create database tables before the first request
@app.before_request
def create_tables():
    db.create_all()

# Function to generate a random ticket number
def generate_ticket_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Since the frontend sends JSON, extract the data accordingly.
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        print(f"Message received from {name} ({email}): {message}")
        return jsonify({"success": True, "message": "Message sent successfully!"})

    return render_template('contact.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        check_in = request.form.get('checkin')
        check_out = request.form.get('checkout')
        room_type = request.form.get('roomType')
        
        # Generate a unique ticket number
        ticket_number = generate_ticket_number()

        # Store reservation in the database
        new_reservation = Reservation(
            name=name,
            email=email,
            check_in=check_in,
            check_out=check_out,
            room_type=room_type,
            ticket_number=ticket_number
        )
        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({"success": True, "message": f"Reservation made successfully! Your ticket number is {ticket_number}"})

    return render_template('reservation.html')

# Admin Login Route
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True  # Store login state
            return redirect(url_for('admin'))
        else:
            flash("Invalid username or password", "danger")

    return render_template('admin_login.html')

# Admin Panel (Restricted)
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        flash("You must be logged in to access the admin panel", "warning")
        return redirect(url_for('admin_login'))

    reservations = Reservation.query.all()
    return render_template('admin.html', reservations=reservations)

# Admin Logout
@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('admin_login'))

port = int(os.environ.get('PORT', 8000))

if __name__ == '__main__':
    # Run the app on 0.0.0.0 and the correct port
    app.run(debug=False, host='0.0.0.0', port=port)
