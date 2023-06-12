from flask_app.config.mysql_connection import connectToMySQL
from flask import flash


class Inventory:
    db_name = "cost_management_db"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.receipts_no = db_data["receipts_no"]
        self.inventory_items_names = db_data["inventory_items_names"]
        self.inventory_items_unit_of_measure = db_data[
            "inventory_items_unit_of_measure"
        ]
        self.inventory_items_id = db_data["inventory_items_id"]
        self.inventory_ledger_id = db_data["inventory_ledger_id"]
        self.supplier_name = db_data["supplier_name"]
        self.document_po = db_data["document_po"]
        self.receipt_qty = db_data["receipt_qty"]
        self.receipt_unit_cost = db_data["receipt_unit_cost"]
        self.receipt_total_cost = db_data["receipt_total_cost"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

    # @classmethod
    # def save_budget(cls, data):
    #     query = "INSERT INTO inventory_receipts (inventory_items_id, project_budgetscol, project_budget_qty, project_budget_unit_cost, project_budget_total_cost) VALUES (%(inventory_items_id)s, %(project_budgetscol)s, %(project_budget_qty)s, %(project_budget_unit_cost)s, %(project_budget_total_cost)s);"
    #     return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_inventory(cls):
        query = "SELECT inventory_receipts.* FROM inventory_receipts"
        results = connectToMySQL(cls.db_name).query_db(query)
        budgets = []
        for result in results:
            ad = cls(result)
            ad.id = result["id"]
            ad.receipts_no = result["receipts_no"]
            ad.inventory_items_names = result["inventory_items_names"]
            ad.inventory_items_unit_of_measure = result[
                "inventory_items_unit_of_measure"
            ]
            ad.inventory_items_id = result["inventory_items_id"]
            ad.inventory_ledger_id = result["inventory_ledger_id"]
            ad.project_budget_qty = result["supplier_name"]
            ad.document_po = result["document_po"]
            ad.receipt_qty = result["receipt_qty"]
            ad.receipt_unit_cost = result["receipt_unit_cost"]
            ad.receipt_total_cost = result["receipt_total_cost"]
            ad.created_at = result["created_at"]
            ad.updated_at = result["updated_at"]
            budgets.append(ad)
        return budgets

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
