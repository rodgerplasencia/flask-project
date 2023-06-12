from flask import flash
from flask_app.config.mysql_connection import connectToMySQL

# from flask_app.models import project

database = "cost_management_db"


class Job_Order:
    def __init__(self, data):
        self.id = data["id"]
        self.quantity = data["quantity"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.job_order_document = None
        self.project_budget = None

    @classmethod
    def get_job_order_documents(cls):
        query = """SELECT job_order_documents.*, projects.project_name, status,
            SUM(job_orders.job_order_qty * inventory_items.unit_cost) AS total_cost
            FROM job_order_documents
            JOIN projects ON job_order_documents.project_id = projects.id
            JOIN job_order_status ON job_order_documents.job_order_status_id = job_order_status.id
            JOIN job_orders ON job_order_documents.id = job_orders.job_order_document_id
            JOIN project_budgets ON job_orders.project_budget_id = project_budgets.id
            JOIN inventory_items ON project_budgets.inventory_items_id = inventory_items.id
            WHERE status = 'pending' OR status = 'approved' GROUP BY job_order_documents.id;"""
        results = connectToMySQL(database).query_db(query)

        job_order_documents = []
        for result in results:
            job_order_document_data = {
                "id": result["id"],
                "document_number": result["document_number"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
                "project_name": result["project_name"],
                "status": result["status"],
                "total_cost": result["total_cost"],
            }
            job_order_document = Job_Order_Document_Summary(job_order_document_data)
            job_order_documents.append(job_order_document)
        return job_order_documents

    @classmethod
    def get_job_order_document(cls, data):
        query = """SELECT * FROM job_order_documents
            LEFT JOIN projects ON job_order_documents.project_id = projects.id
            LEFT JOIN job_order_status ON job_order_documents.job_order_status_id = job_order_status.id
            LEFT JOIN job_orders ON job_order_documents.id = job_orders.job_order_document_id
            LEFT JOIN project_budgets ON job_orders.project_budget_id = project_budgets.id
            LEFT JOIN inventory_items ON project_budgets.inventory_items_id = inventory_items.id
            WHERE job_order_documents.id = %(id)s ORDER BY job_orders.id;"""
        results = connectToMySQL(database).query_db(query, data)
        if len(results) < 1:
            return False

        result = results[0]
        job_order_document_data = {
            "id": result["id"],
            "document_number": result["document_number"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
        job_order_document = Job_Order_Document(job_order_document_data)

        project_data = {
            "id": result["projects.id"],
            "name": result["project_name"],
            "lot_area": result["lot_area"],
            "floor_area": result["floor_area"],
            "location": result["location"],
            "description": result["description"],
            "project_revenue": result["project_revenue"],
            "created_at": result["projects.created_at"],
            "updated_at": result["projects.updated_at"],
        }
        job_order_document.project = Project(project_data)

        job_order_status_data = {
            "id": result["job_order_status.id"],
            "status": result["status"],
            "created_at": result["job_order_status.created_at"],
            "updated_at": result["job_order_status.updated_at"],
        }
        job_order_document.job_order_status = Job_Order_Status(job_order_status_data)

        for result in results:
            job_order_data = {
                "id": result["job_orders.id"],
                "quantity": result["job_order_qty"],
                "created_at": result["job_orders.created_at"],
                "updated_at": result["job_orders.updated_at"],
            }
            job_order = cls(job_order_data)

            project_budget_data = {
                "id": result["project_budgets.id"],
                "quantity": result["project_budget_qty"],
                "created_at": result["project_budgets.created_at"],
                "updated_at": result["project_budgets.updated_at"],
            }
            job_order.project_budget = Project_Budget(project_budget_data)

            inventory_item_data = {
                "id": result["inventory_items.id"],
                "name": result["name"],
                "unit_of_measure": result["unit_of_measure"],
                "quantity": result["qty"],
                "unit_cost": result["unit_cost"],
                "created_at": result["inventory_items.created_at"],
                "updated_at": result["inventory_items.updated_at"],
            }
            job_order.project_budget.inventory_item = Inventory_Item(
                inventory_item_data
            )
            job_order_document.job_orders.append(job_order)
        return job_order_document

    @classmethod
    def get_project_cost(cls, data):
        query = """SELECT SUM(job_orders.job_order_qty * inventory_items.unit_cost) AS project_cost FROM projects
            JOIN job_order_documents ON projects.id = job_order_documents.project_id
            JOIN job_orders ON job_order_documents.id = job_orders.job_order_document_id
            JOIN project_budgets ON job_orders.project_budget_id = project_budgets.id
            JOIN inventory_items ON project_budgets.inventory_items_id = inventory_items.id
            WHERE projects.id = %(id)s GROUP BY projects.id;"""
        results = connectToMySQL(database).query_db(query, data)

        project_cost = results[0]["project_cost"]
        return project_cost if project_cost != None else 0

    @classmethod
    def get_project_budgets(cls, data): # kani na funtion
        query = """SELECT * FROM project_budgets
            JOIN inventory_items ON project_budgets.inventory_items_id = inventory_items.id
            JOIN projects ON project_budgets.project_id = projects.id
            WHERE projects.id = %(id)s ORDER BY project_budgets.id;"""
        results = connectToMySQL(database).query_db(query, data)
        if len(results) < 1:
            return False

        project_budgets = []
        for result in results:
            project_budget_data = {
                "id": result["id"],
                "quantity": result["project_budget_qty"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
            }
            project_budget = Project_Budget(project_budget_data)

            inventory_item_data = {
                "id": result["inventory_items.id"],
                "name": result["name"],
                "unit_of_measure": result["unit_of_measure"],
                "quantity": result["qty"],
                "unit_cost": result["unit_cost"],
                "created_at": result["inventory_items.created_at"],
                "updated_at": result["inventory_items.updated_at"],
            }
            project_budget.inventory_item = Inventory_Item(inventory_item_data)
            project_budgets.append(project_budget)
        return project_budgets

    @classmethod
    def get_projects(cls):
        query = "SELECT * FROM projects;"
        results = connectToMySQL(database).query_db(query)
        if len(results) < 1:
            return False

        projects = []
        for result in results:
            project_data = {
                "id": result["id"],
                "name": result["project_name"],
                "lot_area": result["lot_area"],
                "floor_area": result["floor_area"],
                "location": result["location"],
                "description": result["description"],
                "project_revenue": result["project_revenue"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
            }
            projects.append(Project(project_data))
        return projects

    @classmethod
    def get_project(cls, data):
        query = """SELECT * FROM projects
            JOIN job_order_documents ON projects.id = job_order_documents.project_id
            WHERE job_order_documents.id = %(id)s;"""
        results = connectToMySQL(database).query_db(query, data)
        if len(results) < 1:
            return False

        result = results[0]
        project_data = {
            "id": result["id"],
            "name": result["project_name"],
            "lot_area": result["lot_area"],
            "floor_area": result["floor_area"],
            "location": result["location"],
            "description": result["description"],
            "project_revenue": result["project_revenue"],
            "created_at": result["created_at"],
            "updated_at": result["updated_at"],
        }
        project = Project(project_data)
        return project

    @classmethod
    def save_document(cls, data):
        query = """INSERT INTO job_order_documents (project_id, job_order_status_id) VALUES (%(id)s,
            (SELECT id FROM job_order_status WHERE status = 'new'));"""
        document_id = connectToMySQL(database).query_db(query, data)

        data = {"id": document_id}
        # query = """UPDATE job_order_documents SET document_number = CONCAT(YEAR(NOW()), "-", LPAD(LAST_INSERT_ID(), 6, '0')) WHERE id = LAST_INSERT_ID();"""
        query = """UPDATE job_order_documents SET document_number = CONCAT(YEAR(NOW()), "-", LPAD(%(id)s, 6, '0')) WHERE id = %(id)s;"""
        connectToMySQL(database).query_db(query, data)
        return document_id

    @classmethod
    def save_job_order(cls, data):
        query = """INSERT INTO job_orders (job_order_qty, job_order_document_id, project_budget_id)
            VALUES (%(quantity)s, %(document_id)s, %(project_budget_id)s);"""
        return connectToMySQL(database).query_db(query, data)

    @classmethod
    def set_pending(cls, data):
        query = """UPDATE job_order_documents SET job_order_status_id =
        (SELECT id FROM job_order_status WHERE status = 'pending') WHERE id = %(id)s;"""
        return connectToMySQL(database).query_db(query, data)

    @classmethod
    def set_approved(cls, data):
        query = """UPDATE job_order_documents SET job_order_status_id =
        (SELECT id FROM job_order_status WHERE status = 'approved') WHERE id = %(id)s;"""
        return connectToMySQL(database).query_db(query, data)

    @classmethod
    def delete_job_order(cls, data):
        query = "DELETE FROM job_orders WHERE id = %(id)s;"
        return connectToMySQL(database).query_db(query, data)


class Project:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.lot_area = data["lot_area"]
        self.floor_area = data["floor_area"]
        self.location = data["location"]
        self.description = data["description"]
        self.project_revenue = data["project_revenue"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.project_budgets = []
        self.job_order_documents = []


class Project_Budget:
    def __init__(self, data):
        self.id = data["id"]
        self.quantity = data["quantity"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.inventory_item = None


class Inventory_Item:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.unit_of_measure = data["unit_of_measure"]
        self.quantity = data["quantity"]
        self.unit_cost = data["unit_cost"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


class Job_Order_Status:
    def __init__(self, data):
        self.id = data["id"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


class Job_Order_Document:
    def __init__(self, data):
        self.id = data["id"]
        self.document_number = data["document_number"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.project = None
        self.job_order_status = None
        self.job_orders = []


# query = """SELECT job_order_documents.id, job_order_documents.document_number, job_order_documents.created_at, job_order_documents.updated_at,
#             project.name, job_order_status.status, SUM(job_orders.job_order_qty * inventory_items.unit_cost) AS total_cost
class Job_Order_Document_Summary:
    def __init__(self, data):
        self.id = data["id"]
        self.document_number = data["document_number"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.project_name = data["project_name"]
        self.status = data["status"]
        self.total_cost = data["total_cost"]

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE job_orders SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, made_on = %(made_on)s, under_30_minutes = %(under_30_minutes)s, has_chicken = %(has_chicken)s, has_beef = %(has_beef)s, has_pork = %(has_pork)s, cuisine = %(cuisine)s, price = %(price)s, image_url = %(image_url)s, updated_at = NOW() WHERE id = %(id)s;"
    #     return connectToMySQL(database).query_db(query, data)

    # @classmethod
    # def delete(cls, data):
    #     query = "DELETE FROM job_orders WHERE id = %(id)s;"
    #     return connectToMySQL(database).query_db(query, data)

    # @classmethod
    # def validate(cls, data):
    #     is_valid = True

    #     if len(data['name'].strip()) < 1:
    #         flash("Name is required!", 'name')
    #         is_valid = False
    #     elif len(data['name'].strip()) < 3:
    #         flash("Name must be at least 3 characters!", 'name')
    #         is_valid = False
    #     elif cls.get_by_name(data):
    #         flash("Name is already taken!", 'name')
    #         is_valid = False

    #     if len(data['description'].strip()) < 1:
    #         flash("Description is required!", 'description')
    #         is_valid = False
    #     elif len(data['description'].strip()) < 3:
    #         flash("Description must be at least 3 characters!", 'description')
    #         is_valid = False

    #     if len(data['instructions'].strip()) < 1:
    #         flash("Instructions is required!", 'instructions')
    #         is_valid = False
    #     elif len(data['instructions'].strip()) < 3:
    #         flash("Instructions must be at least 3 characters!", 'instructions')
    #         is_valid = False

    #     if len(data['made_on']) < 1:
    #         flash("Date Made On is required!", 'made_on')
    #         is_valid = False
    #     elif datetime.strptime(data['made_on'], "%Y-%m-%d").date() > datetime.now().date():
    #         flash("Date Made On must not be in the future!", 'made_on')
    #         is_valid = False

    #     if not data.get('under_30_minutes'):
    #         flash("Under 30 Minutes is required!", 'under_30_minutes')
    #         is_valid = False

    #     if len(data['cuisine']) < 1:
    #         flash("Cuisine is required!", 'cuisine')
    #         is_valid = False

    #     if len(data['price']) < 1:
    #         flash("Price is required!", 'price')
    #         is_valid = False

    #     if len(data['image_url'].strip()) < 1:
    #         flash("Image URL is required!", 'image_url')
    #         is_valid = False

    #     return is_valid


# class User:
#     def __init__(self, data):
#         self.id = data['id']
#         self.first_name = data['first_name']
#         self.last_name = data['last_name']
#         self.email = data['email']
#         self.password = data['password']
#         self.created_at = data['created_at']
#         self.updated_at = data['updated_at']

# class Role:
#     def __init__(self, data):
#         self.id = data['id']
#         self.name = data['name']
#         self.created_at = data['created_at']
#         self.updated_at = data['updated_at']


# query = """SELECT * FROM job_order_documents
#     JOIN projects ON job_order_documents.project_id = projects.id
#     JOIN job_order_status ON job_order_documents.job_order_status_id = job_order_status.id
#     JOIN job_orders ON job_order_documents.id = job_orders.job_order_document_id
#     JOIN project_budgets ON job_orders.project_budget_id = project_budgets.id
#     JOIN inventory_items ON project_budgets.inventory_items_id = inventory_items.id
#     ORDER BY job_order_documents.id;"""

# job_order_document_data = {
#     'id': result['id'],
#     'document_number': result['document_number'],
#     'created_at': result['created_at'],
#     'updated_at': result['updated_at']
# }
# job_order_document = Job_Order_Document(job_order_document_data)

# project_data = {
#     'id': result['projects.id'],
#     'name': result['project_name'],
#     'lot_area': result['lot_area'],
#     'floor_area': result['floor_area'],
#     'location': result['location'],
#     'description': result['description'],
#     'project_revenue': result['project_revinue'],
#     'created_at': result['projects.created_at'],
#     'updated_at': result['projects.updated_at']
# }
# job_order_document.project = Project(project_data)

# job_order_data = {
#     'id': result['id'],
#     'quantity': result['job_order_qty'],
#     'created_at': result['created_at'],
#     'updated_at': result['updated_at']
# }
# job_order = cls(job_order_data)

# project_budget_data = {
#     'id': result['project_budgets.id'],
#     'quantity': result['project_budget_qty'],
#     'created_at': result['project_budgets.created_at'],
#     'updated_at': result['project_budgets.updated_at']
# }
# job_order.project_budget = Project_Budget(project_budget_data)

# inventory_item_data = {
#     'id': result['inventory_items.id'],
#     'name': result['name'],
#     'unit_of_measure': result['unit_of_measure'],
#     'quantity': result['qty'],
#     'unit_cost': result['unit_cost'],
#     'created_at': result['inventory_items.created_at'],
#     'updated_at': result['inventory_items.updated_at']
# }
# job_order.project_budget.inventory_item = Inventory_Item(inventory_item_data)
