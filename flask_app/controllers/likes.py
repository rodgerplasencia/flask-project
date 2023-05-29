from flask import render_template, redirect, request, session, flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.like import Like


def check_session():
    if "user_id" not in session:
        return redirect("/logout")


@app.route("/post/like/<int:id>")
def post_like(id):
    check_session()

    data = {"user_id": session["user_id"], "post_id": id}
    # Like.save_like(data)
    Like.validate_likes(data)
    return redirect("/dashboard")
