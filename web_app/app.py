from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_app_data.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)


@app.route("/")
def index():
    """Hello World. Totally monotonous and boring."""
    return render_template("homepage.html")


@app.route("/about")
def about():
    return "About Me"


@app.route("/users")
@app.route("/users.json")
def users():
    users = [
        {"id": 1, "name": "First"},
        {"id": 2, "name": "Second"},
        {"id": 3, "name": "third"}
    ]
    return jsonify(users)


@app.route("/users/create", methods=["POST"])
def create_user():
    print("CREATING A NEW USER...")
    print("FORM DATA:", dict(request.form))
    # todo: create a new user
    return jsonify({"message": "CREATED OK (TODO)"})
