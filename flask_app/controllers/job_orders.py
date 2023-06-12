from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.job_order import Job_Order
from flask_app.models.user import User


@app.route("/job_orders")
def job_orders_index():
    # if not 'id' in session:
    #     return redirect('/')
    return render_template(
        "job_orders/index.html",
        documents=Job_Order.get_job_order_documents(),
        user=User.get_by_id({"id": session["user_id"]}),
    )


@app.route("/job/orders")
def jobOrders():
    # if not "id" in session:
    #     return redirect("/")

    return render_template(
        "job_order.html",
        projects=Job_Order.get_projects(),
        status="init",
        documents=Job_Order.get_job_order_documents(),
        user=User.get_by_id({"id": session["user_id"]}),
    )


@app.route("/job_orders/new")
def job_orders_new_init():
    # if not 'id' in session:
    #     return redirect('/')
    return render_template(
        "job_orders/new.html",
        projects=Job_Order.get_projects(),
        status="init",
        user=User.get_by_id({"id": session["user_id"]}),
    )


@app.route("/job_orders/new", methods=["POST"])
def job_orders_new_document():
    document_id = Job_Order.save_document({"id": request.form["project_id"]})
    return redirect("/job_orders/new/documents/" + str(document_id))


@app.route("/job_orders/new/documents/<int:id>")
def job_orders_new(id):
    # if not 'id' in session:
    #     return redirect('/')
    project = Job_Order.get_project({"id": id})
    return render_template(
        "job_orders/new.html",
        document=Job_Order.get_job_order_document({"id": id}),
        project_budgets=Job_Order.get_project_budgets({"id": project.id}),
        status="new",
        user=User.get_by_id({"id": session["user_id"]}),
    )


@app.route("/job_orders/new/documents/<int:id>", methods=["POST"])
def job_orders_new_job_order(id):
    # if not Job_Order.validate(request.form):
    #     return redirect('/job_orders/new')
    data = {
        "quantity": request.form["quantity"],
        "document_id": id,
        "project_budget_id": request.form["project_budget_id"],
    }
    Job_Order.save_job_order(data)
    return redirect("/job_orders/new/documents/" + str(id))


@app.route("/job_orders/pending/documents/<int:id>", methods=["POST"])
def job_orders_set_pending(id):
    Job_Order.set_pending({"id": id})
    return redirect("/job_orders")


@app.route("/job_orders/pending/documents/<int:id>")
def job_orders_pending(id):
    # if not 'id' in session:
    #     return redirect('/')
    project = Job_Order.get_project({"id": id})
    return render_template(
        "job_orders/new.html",
        document=Job_Order.get_job_order_document({"id": id}),
        project_budgets=Job_Order.get_project_budgets({"id": project.id}),
        status="pending",
        user=User.get_by_id({"id": session["user_id"]}),
    )


@app.route("/job_orders/approved/documents/<int:id>", methods=["POST"])
def job_orders_set_approved(id):
    Job_Order.set_approved({"id": id})
    return redirect("/job_orders")


@app.route("/job_orders/approved/documents/<int:id>")
def job_orders_approved(id):
    # if not 'id' in session:
    #     return redirect('/')
    project = Job_Order.get_project({"id": id})
    return render_template(
        "job_orders/show.html",
        document=Job_Order.get_job_order_document({"id": id}),
        project_cost=Job_Order.get_project_cost({"id": project.id}),
        user=User.get_by_id({"id": session["user_id"]}),
    )


@app.route(
    "/job_orders/new/documents/<int:document_id>/delete/job_orders/<int:job_order_id>",
    methods=["POST"],
)
def job_orders_delete_job_order(document_id, job_order_id):
    Job_Order.delete_job_order({"id": job_order_id})
    return redirect("/job_orders/new/documents/" + str(document_id))


# @app.route('/job_orders/edit/<int:id>')
# def edit(id):
#     # if not 'id' in session:
#     #     return redirect('/')
#     recipe = Job_Order.get_one({'id': id})
#     if Job_Order.user.id != session['id']:
#         return redirect('/dashboard')
#     return render_template('edit.html', recipe=recipe, user=User.get_one(session))

# @app.route('/update/<string:id>', methods=['POST'])
# def update(id):
#     if not Job_Order.validate(request.form):
#         return redirect('/job_orders/edit/' + id)
#     data = {
#         'id': request.form['id'],
#         'name': request.form['name'].strip(),
#         'description': request.form['description'].strip(),
#         'instructions': request.form['instructions'].strip(),
#         'made_on': request.form['made_on'],
#         'under_30_minutes': request.form['under_30_minutes'],
#         'has_chicken': 1 if request.form.get('has_chicken') else 0,
#         'has_beef': 1 if request.form.get('has_beef') else 0,
#         'has_pork': 1 if request.form.get('has_pork') else 0,
#         'cuisine': request.form['cuisine'],
#         'price': request.form['price'],
#         'image_url': request.form['image_url']
#     }
#     Job_Order.update(data)
#     # Job_Order.update(request.form)
#     return redirect('/dashboard')

# @app.route('/delete/<int:id>', methods=['POST'])
# def delete(id):
#     Job_Order.delete({'id': id})
#     return redirect('/dashboard')
