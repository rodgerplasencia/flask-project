from flask import render_template, redirect, request, session, flash
import re
from flask_bcrypt import Bcrypt

from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.address import Address


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


@app.route("/add/budget")
def view_budget_form():
    check_session()
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    data = {"id": session["user_id"]}
    return render_template("add_budget_items.html", user=User)


# @app.route("/edit/book/<int:id>", methods=["POST", "GET"])
# def edit_book(id):
#     check_session()

#     data = {"id": id}
#     user_data = {"id": session["user_id"]}
#     return render_template(
#         "edit_book.html", edit=Book.get_one(data), user=User.get_by_id(user_data)
#     )


# @app.route("/update/book", methods=["POST"])
# def update_book():
#     check_session()
#     if not Book.validate_book(request.form):
#         return redirect("/new/book")
#     data = {
#         "title": request.form["title"],
#         "description": request.form["description"],
#         "id": request.form["id"],
#     }
#     Book.update(data)
#     return redirect("/dashboard")


# @app.route("/book/<int:id>")
# def show_book(id):
#     check_session()
#     data = {"id": id}
#     book_id = {"book_id": id}
#     user_data = {"id": session["user_id"]}
#     book_likers = Like.get_likers_book(book_id)
#     return render_template(
#         "book_details.html",
#         book=Book.get_one(data),
#         user=User.get_by_id(user_data),
#         book_likers=book_likers,
#     )


# @app.route("/post/delete/<int:id>", methods=["POST", "GET"])
# def delete_post(id):
#     check_session()
#     data = {"id": id}
#     Post.delete(data)
#     return redirect("/dashboard")


# @app.route("/post/likes/<int:id>", methods=["POST", "GET"])
# def liked_post(id):
#     check_session()
#     data = {"id": id}
#     one_post = Post.get_one(data)
#     return render_template("post_likes.html", one_post=one_post)


# @app.route("/viewer/<int:id>")
# def show_liker(id):
#     check_session()
#     data = {"id": id}
#     data_book_id = {"book_id": id}
#     book_id = {"book_id": id}
#     user_data = {"id": session["user_id"]}
#     likers = Like.get_likers_book(data_book_id)
#     return render_template(
#         "viewer.html",
#         book=Book.get_one(data),
#         user=User.get_by_id(user_data),
#         book_likers=likers,
#     )
