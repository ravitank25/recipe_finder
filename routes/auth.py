from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

auth_bp = Blueprint(
    "auth",
    __name__
)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validation
        if not username or len(username) < 3:
            flash("Username must be at least 3 characters.", "error")
            return render_template("signup.html")
        
        if not email or "@" not in email:
            flash("Please enter a valid email.", "error")
            return render_template("signup.html")
        
        if not password or len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return render_template("signup.html")
        
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("signup.html")
        
        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "error")
            return render_template("signup.html")
        
        try:
            hashed_password = generate_password_hash(password)
            user = User(
                username=username,
                email=email,
                password=hashed_password
            )
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again.", "error")
    
    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template("login.html")
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect("/")
        else:
            flash("Invalid email or password.", "error")
    
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect("/")