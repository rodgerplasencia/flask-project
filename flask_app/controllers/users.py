from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.address import Address
from flask_app.models.project_budget import Budget
from flask_app.models.inventory import Inventory
from flask_app.models.job_order1 import Job_order1
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
    return redirect("/waiting/approval")


@app.route("/login", methods=["POST"])
def login():
    data = {"email": request.form["email"]}
    user = User.get_by_email(data)

    if not user:
        flash("invalid Email/Password", "login")
        return redirect("/")
    if user.status == "unverified":
        flash("Waiting for Approval", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid Password", "login")
        return redirect("/")
    # if ok ang session  sa dashboard ang punta
    session["user_id"] = user.id
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    check_session()
    data = {"id": session["user_id"]}
    data_id = {"user_id": session["user_id"]}
    user = User.get_by_id(data)
    job_sum = Job_order1.get_job_order()
    bud_rev = Job_order1.get_bud_revenue()

    chart_data = {
        "labels": [job.project_name for job in job_sum],
        "datasets": [
            {
                "data": [job.total_cost_per_project for job in job_sum],
                "backgroundColor": ["#ff6384", "#36a2eb", "#ffce56"],
            }
        ],
    }
    chart_data2 = {
        "labels": [bud.project_name for bud in bud_rev],
        "datasets": [
            {
                "data": [bud.bud_revenue for bud in bud_rev],
                "backgroundColor": ["#ff6384", "#36a2eb", "#ffce56"],
            }
        ],
    }

    return render_template(
        "dashboard.html", user=user, chart_data=chart_data, chart_data2=chart_data2
    )


@app.route("/waiting/approval")
def nre_reg():
    check_session()
    data = {"id": session["user_id"]}
    data_id = {"user_id": session["user_id"]}
    user = User.get_by_id(data)
    return render_template("pre_approve.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/employee/status")
def employees_dasbord():
    check_session()
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    employees = User.get_employee_status()
    return render_template("employees_status.html", employees=employees, user=user)


@app.route("/updated/status", methods=["POST"])
def updated_user_status():
    data = {"id": request.form["id"], "status": request.form["status"]}
    User.update_status(data)
    return redirect("/employee/status")
