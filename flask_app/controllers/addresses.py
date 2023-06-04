from flask import render_template, redirect, request, session, flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.address import Address
from flask_app.models.project_budget import Budget


def check_session():
    if "user_id" not in session:
        return redirect("/logout")


@app.route("/project/address")
def view_address():
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    data = {"id": session["user_id"]}
    address = Address.get_project_address()
    return render_template("project_address.html", user=user, address=address)


@app.route("/project/add/address", methods=["POST"])
def create_address():
    check_session()
    data = {
        "address": request.form["address"],
        "barangay": request.form["barangay"],
    }
    Address.save_add(data)
    data_user = {"id": session["user_id"]}
    user = User.get_by_id(data_user)
    return redirect("/project/address")


@app.route("/print")
def view_print():
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    data = {"id": session["user_id"]}
    budgets = Budget.get_budget()
    return render_template("data-print.html", user=user, budgets=budgets)
