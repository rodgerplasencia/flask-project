from flask_app import app
from flask_app.controllers import projects, users, addresses


if __name__ == "__main__":
    app.run(debug=True)
