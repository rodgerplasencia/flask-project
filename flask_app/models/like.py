from flask_app.config.mysql_connection import connectToMySQL
from flask import flash

class Like:
    db_name = 'like_wireframe'
    
    def __init__(self, db_data):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.post_id = db_data['post_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save_like(cls, data):
        query = "INSERT INTO likes (user_id, post_id, updated_at) VALUES (%(user_id)s, %(post_id)s, NOW());"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_likers_book(cls, data):
        query = "SELECT CONCAT(users.firstname, ' ', users.lastname) AS name, likes.* FROM likes LEFT JOIN users ON users.id = likes.user_id WHERE likes.book_id = %(book_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likers = []
        for liker in results:
            likers.append(liker)
        return likers
    

    @classmethod
    def remove(cls, data):
        query = "DELETE FROM likes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_by_post(cls,data):
        query = "SELECT*FROM likes WHERE user_id = %(user_id)s and post_id = %(post_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_likes(data):
        query = "SELECT * FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s;"
        results = connectToMySQL(Like.db_name).query_db(query, data)
        if len(results) >= 1:
            flash("You have already liked this book.", "like")
            return False
        else:
            Like.save_like(data)
            return True