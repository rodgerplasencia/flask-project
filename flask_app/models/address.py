from flask_app.config.mysql_connection import connectToMySQL
from flask import flash


class Address:
    db_name = "cost_management_db"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.complete_address = db_data["complete_address"]
        self.barangay = db_data["barangay"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    @classmethod
    def save_add(cls, data):
        query = "INSERT INTO project_address (complete_address, barangay) VALUES (%(address)s, %(barangay)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_project_address(cls):
        query = "SELECT project_address.* FROM project_address"
        results = connectToMySQL(cls.db_name).query_db(query)
        address = []
        for result in results:
            ad = cls(result)
            ad.id = result["id"]
            ad.complete_address = result["complete_address"]
            ad.barangay = result["barangay"]
            ad.created_at = result["created_at"]
            ad.updated_at = result["updated_at"]
            address.append(ad)
        return address

    # @classmethod
    # def get_likers_book(cls, data):
    #     query = "SELECT CONCAT(users.firstname, ' ', users.lastname) AS name, likes.* FROM likes LEFT JOIN users ON users.id = likes.user_id WHERE likes.book_id = %(book_id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     likers = []
    #     for liker in results:
    #         likers.append(liker)
    #     return likers

    # @classmethod
    # def remove(cls, data):
    #     query = "DELETE FROM likes WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod
    # def get_by_post(cls,data):
    #     query = "SELECT*FROM likes WHERE user_id = %(user_id)s and post_id = %(post_id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     print(results)
    #     if len(results) < 1:
    #         return False
    #     return cls(results[0])

    # @staticmethod
    # def validate_likes(data):
    #     query = "SELECT * FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
    #     results = connectToMySQL(Like.db_name).query_db(query, data)
    #     if len(results) >= 1:
    #         flash("You have already liked this book.", "like")
    #         return False
    #     else:
    #         Like.save_like(data)
    #         return True
