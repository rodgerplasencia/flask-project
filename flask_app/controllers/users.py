from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.like import Like
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


def check_session():
    if "user_id" not in session:
        return redirect("/logout")


###################################################################################


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register")
def sign_up():
    return render_template("registration.html")


# para sa sign-up
@app.route("/register", methods=["POST"])
def register():
    is_valid = User.validate_register(request.form)
    if not is_valid:
        return render_template("registration.html")
    new_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    id = User.save(new_user)  # para masave sa database
    if not id:
        flash("Email is allready taken.", "register")
        return render_template("registration.html")
    session["user_id"] = id
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    data = {"email": request.form["email"]}
    user = User.get_by_email(data)

    if not user:
        flash("invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid Password", "login")
        return redirect("/")
    # if ok ang session  sa dashboard ang punta
    session["user_id"] = user.id
    return redirect("/dashboard")


# dashboard------------------------
@app.route("/dashboard")
def dashboard():
    check_session()
    data = {"id": session["user_id"]}
    data_id = {"user_id": session["user_id"]}
    user = User.get_by_id(data)
    posts = Project.get_user_post(data_id)

    return render_template("dashboard.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# dashboard------------------------
@app.route("/employee/status")
def employees_dasbord():
    check_session()
    data = {"id": session["user_id"]}
    employees = User.get_employee_status()
    user = User.get_by_id(data)
    return render_template("employees_status.html", employees=employees, user=user)


@app.route("/updated/status", methods=["POST"])
def updated_user_status():
    data = {"id": request.form["id"], "status": request.form["status"]}
    User.update_status(data)
    return redirect("/employee/status")
