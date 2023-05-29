from flask_app.config.mysql_connection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

from flask import flash


class User:
    db_name = "cost_management_db"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.first_name = db_data["first_name"]
        self.last_name = db_data["last_name"]
        self.email = db_data["email"]
        self.moblie = db_data["mobile"]
        self.password = db_data["password"]
        self.job_title = db_data["job_title"]
        self.job_department = db_data["job_department"]
        self.immediate_supervisor = db_data["immediate_supervisor"]
        self.status = db_data["status"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    @classmethod  # save data
    def save(cls, data):
        query = "INSERT INTO employees(first_name,last_name,email,password)VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod # call para sa table
    # def get_all(cls):
    #     query = "SELECT users.first_name as firstname, users.last_name as lastname, books* FROM users LEFT JOIN books ON WHERE users.id=books.author_id;"
    #     results = connectToMySQL(cls.db_name).query_db(query)
    #     users = []
    #     for user in results:
    #         users.append(cls(user))
    #     return users

    @classmethod  # individual call pwede sa validation
    def get_one(cls, data):
        query = "SELECT*FROM employees WHERE id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod  # call sa email
    def get_by_email(cls, data):
        query = "SELECT*FROM employees WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        print(results)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod  # call sa individual id
    def get_by_id(cls, data):
        query = "SELECT*FROM employees WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @staticmethod  # validation sa register
    def validate_register(user):
        is_valid = True
        query = "SELECT*FROM employees WHERE email=%(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, user)
        if len(results) >= 1:
            flash("Email is already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email!!", "register")
            is_valid = False
        if len(user["first_name"]) < 3:
            flash("First name must be at lest 3 characters", "register")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at lest 3 characters", "register")
            is_valid = False
        if len(user["password"]) < 0:
            flash("Password must be at lest 10 characters", "register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Password don't match ", "register")
        return is_valid

    @classmethod
    def get_employee_status(
        cls,
    ):
        query = "SELECT employees.* FROM employees"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for result in results:
            user = cls(result)
            user.first_name = result["first_name"]
            user.last_name = result["last_name"]
            user.email = result["email"]
            user.address = result["address"]
            user.status = result["status"]
            users.append(user)
        return users

    @classmethod
    def update_status(cls, data):
        query = "UPDATE employees SET status=%(status)s WHERE id=%(id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)
