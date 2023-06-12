from flask import render_template, redirect, request, session, flash
import re
from flask_bcrypt import Bcrypt

from flask_app import app
import os
import pandas as pd
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.address import Address
from flask_app.models.project_budget import Budget
from flask_app.models.inventory import Inventory


def check_session():
    if "user_id" not in session:
        return redirect("/logout")


@app.route("/project")
def view_project():
    check_session()
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    data = {"id": session["user_id"]}
    address = Address.get_project_address()
    return render_template("project.html", user=user, address=address)


@app.route("/add/project", methods=["POST"])
def add_project():
    check_session()
    project_data = {
        "project_name": request.form["project_name"],
        "lot_area": request.form["lot_area"],
        "floor_area": request.form["floor_area"],
        "location": request.form["location"],
        "description": request.form["description"],
        "project_revinue": request.form["project_revinue"],
        "project_address_id": request.form["address_id"],
    }
    Project.save(project_data)
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    return render_template("project.html", user=User)


@app.route("/save/budget", methods=["POST"])
def save_budgets():
    check_session()
    budget_data = {
        "inventory_items_id": request.form["inventory_items_id"],
        "project_budgetscol": request.form["project_budgetscol"],
        "project_budget_qty": request.form["qty"],
        "project_budget_unit_cost": request.form["unit_cost"],
        "project_budget_total_cost": request.form["total_cost"],
    }
    Budget.save_budget(budget_data)
    return redirect("/budget")


@app.route("/budget")
def view_budget_form():
    check_session()
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    budgets = Budget.get_budget()
    return render_template("add_budget_items.html", user=user, budgets=budgets)


@app.route("/export")
def export():
    budgets = Budget.get_budget()
    data = []

    for budget in Budget.get_budget():
        data.append(
            [
                budget.inventory_items_id,
                budget.project_budgetscol,
                budget.project_budget_qty,
                budget.project_budget_unit_cost,
            ]
        )

    df = pd.DataFrame(
        data,
        columns=[
            "inventory_items_id",
            "project_budgetscol",
            "project_budget_qty",
            "project_budget_unit_cost",
        ],
    )
    directory = "download"
    df.to_excel(os.path.join(directory, "Budget-table.xlsx"), index=False)
    return redirect("/budget")


@app.route("/inventory")
def inventory():
    check_session()
    data = {"id": session["user_id"]}
    data_id = {"user_id": session["user_id"]}
    user = User.get_by_id(data)
    inventories = Inventory.get_inventory()

    return render_template("inventory.html", user=user, inventories=inventories)


@app.route("/report")
def view_report():
    check_session()
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    data = {"id": session["user_id"]}
    address = Address.get_project_address()
    return render_template("report.html", user=user)


@app.route("/inventory/print")
def inventory_print():
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    inventories = Inventory.get_inventory()
    return render_template("inventory-print.html", user=user, inventories=inventories)
