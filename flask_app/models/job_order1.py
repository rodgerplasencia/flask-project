from flask_app.config.mysql_connection import connectToMySQL
from flask import flash

# from datetime import datetime
# import math
import re


class Job_order1:
    db_name = "cost_management_db"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.job_order_document = db_data.get("job_order_document")
        self.project_name = db_data["project_name"]
        self.inventory_items_name = db_data.get("inventory_items_name")
        self.inventory_items_unit_of_measure = db_data.get(
            "inventory_items_unit_of_measure"
        )
        self.job_order_actual_qty = db_data.get("job_order_actual_qty")
        self.job_order_actual_unitcost = db_data.get("job_order_actual_unitcost")
        self.job_order_actual_totalcost = db_data.get("job_order_actual_totalcost")
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    @classmethod
    def get_job_order(cls):
        query = "SELECT  SUM(job_orders_1.job_order_actual_unitcost) AS total_cost_per_project ,job_orders_1.* FROM job_orders_1  GROUP BY job_orders_1.project_name;"

        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            jobs = []
            for result in results:
                job = cls(result)
                job.total_cost_per_project = result["total_cost_per_project"]
                job.id = result["id"]
                job.project_name = result["project_name"]
                jobs.append(job)
            return jobs

    @classmethod
    def get_bud_revenue(cls):
        query = "SELECT  projects.* FROM projects;"

        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            bud_revenues = []
            for result in results:
                bud = cls(result)
                bud.id = result["id"]
                bud.bud_revenue = result["bud_revenue"]
                bud.project_name = result["project_name"]
                bud_revenues.append(bud)
            return bud_revenues

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
