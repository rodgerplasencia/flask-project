from flask_app.config.mysql_connection import connectToMySQL
from flask import flash

# from datetime import datetime
# import math
import re


class Project:
    db_name = "cost_management_db"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.project_name = db_data["project_name"]
        self.lot_area = db_data["lot_area"]
        self.floor_area = db_data["floor_area"]
        self.location = db_data["location"]
        self.description = db_data["description"]
        self.project_revinue = db_data["project_revinue"]
        self.project_address_id = db_data["project_address_id"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    # def time_span(self):
    #     now = datetime.now()
    #     delta = now - self.created_at
    #     print(delta.days)
    #     print(delta.total_seconds())
    #     if delta.days > 0:
    #         return f"{delta.days} days ago"
    #     elif (math.floor(delta.total_seconds()/60)) >=60:
    #         return f"{math.floor(math.floor(delta.total_seconds()/60)/60)} hours ago"
    #     elif delta.total_seconds()>=60:
    #         return f"{math.floor(delta.total_seconds()/60)} minutes ago"
    #     else:
    #         return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def save(cls, data):
        query = "INSERT INTO projects (project_name, lot_area, floor_area, location, description, project_revinue,project_address_id)VALUES(%(project_name)s, %(lot_area)s,  %(floor_area)s, %(location)s, %(description)s, %(project_revinue)s, %(project_address_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod  # individual na tawag
    # def get_one(cls, data):
    #     query = "SELECT*FROM posts WHERE id=%(id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     if results:
    #         return cls(results[0])
    #     else:
    #         return None

    # @classmethod  # update
    # def update(cls, data):
    #     query = "UPDATE posts SET post=%(post)s, WHERE id=%(id)s"
    #     return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod
    # def get_user_post(cls, data):
    #     query = "SELECT users.id AS user_id, users.firstname AS name, posts.id AS post_id, posts.post AS post, posts.created_at AS created_at, posts.updated_at AS updated_at, COUNT(likes.user_id) AS likes_count,likes.* FROM posts LEFT JOIN users ON users.id = posts.user_id LEFT JOIN likes ON likes.post_id = posts.id GROUP BY posts.id;"

    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     if results:
    #         posts = []
    #         for result in results:
    #             post = cls(result)
    #             post.name = result["name"]
    #             post.id = result["id"]
    #             post.user_id = result["user_id"]
    #             post.post = result["post"]
    #             post.created_at = result["created_at"]
    #             post.updated_at = result["updated_at"]
    #             post.likes_count = result["likes_count"]
    #             posts.append(post)
    #         return posts

    # @classmethod  # delete
    # def delete(cls, data):
    #     query = "DELETE FROM posts WHERE id = %(id)s;"
    #     # query = "DELETE FROM likes WHERE post_id = %(id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)

    1
    # def validate_book(book):
    #     is_valid = True
    #     if len(book['title'])<3:
    #         flash("Title must be at least 3 characters.","book")
    #     if len(book['description'])<3:
    #         flash("Description must be at least 3 characters.","book")
    #         is_valid=False
    #     return is_valid
