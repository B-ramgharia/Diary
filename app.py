import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-premium-secret-key-12345")

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))

# Use DATABASE_URL from environment for production, fallback to SQLite for local development
db_url = os.getenv("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    # Fix for SQLAlchemy 1.4+ which requires 'postgresql://' instead of 'postgres://'
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or ('sqlite:///' + os.path.join(basedir, 'diary.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    entries = db.relationship('Entry', backref='owner', lazy=True, cascade="all, delete-orphan")

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), index=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

with app.app_context():
    db.create_all()

# Auth Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login'))
            
        # Verify user still exists in DB (handles case where DB was reset or user deleted)
        user = db.session.get(User, session['user_id'])
        if not user:
            session.clear()
            flash("Session expired or user not found. Please login again.", "error")
            return redirect(url_for('login'))
            
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route("/")
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash("Email or Username already exists.", "error")
            return redirect(url_for('register'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.hashed_password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('dashboard'))
        
        flash("Invalid email or password.", "error")
        return redirect(url_for('login'))
        
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route("/dashboard")
@login_required
def dashboard():
    # User is guaranteed to exist by the decorator
    user = db.session.get(User, session['user_id'])
    entries = Entry.query.filter_by(owner_id=user.id).order_by(Entry.created_at.desc()).all()
    return render_template("dashboard.html", entries=entries)

# Entry CRUD
@app.route("/entries", methods=["POST"])
@login_required
def create_entry():
    title = request.form.get("title")
    content = request.form.get("content")
    
    if not title or not content:
        flash("Title and Content are required.", "error")
        return redirect(url_for('dashboard'))
        
    new_entry = Entry(title=title, content=content, owner_id=session['user_id'])
    db.session.add(new_entry)
    db.session.commit()
    
    flash("New reflection saved successfully!", "success")
    return redirect(url_for('dashboard'))

@app.route("/entries/<int:entry_id>/edit", methods=["POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id, owner_id=session['user_id']).first()
    if not entry:
        flash("Entry not found.", "error")
        return redirect(url_for('dashboard'))
        
    entry.title = request.form.get("title")
    entry.content = request.form.get("content")
    db.session.commit()
    
    flash("Reflection updated!", "success")
    return redirect(url_for('dashboard'))

@app.route("/entries/<int:entry_id>/delete", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.filter_by(id=entry_id, owner_id=session['user_id']).first()
    if not entry:
        flash("Entry not found.", "error")
        return redirect(url_for('dashboard'))
        
    db.session.delete(entry)
    db.session.commit()
    
    flash("Reflection deleted.", "success")
    return redirect(url_for('dashboard'))

@app.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    password = request.form.get("password")
    user = db.session.get(User, session['user_id'])
    
    if not bcrypt.check_password_hash(user.hashed_password, password):
        flash("Incorrect password. Account deletion failed.", "error")
        return redirect(url_for('dashboard'))
        
    db.session.delete(user)
    db.session.commit()
    session.clear()
    
    flash("Your account has been permanently deleted.", "success")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
