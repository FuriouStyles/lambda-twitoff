from flask import Blueprint, jsonify, request, current_app, render_template
from organized_app.models import User, Tweet
from web_app.twitter_service.py import twitter_api_client
my_routes = Blueprint("my_routes", __name__)

@app.route("/")
def index():
    """Hello World. Totally monotonous and boring."""
    return render_template("homepage.html")


@my_routes.route("/about")
def about():
    return "About Me"


@my_routes.route("/users")
@my_routes.route("/users.json")
def users():
    users = [
        {"id": 1, "name": "First"},
        {"id": 2, "name": "Second"},
        {"id": 3, "name": "third"}
    ]
    return jsonify(users)


@my_routes.route("/users/create", methods=["POST"])
def create_user():
    print("CREATING A NEW USER...")
    print("FORM DATA:", dict(request.form))
    # todo: create a new user
    return jsonify({"message": "CREATED OK (TODO)"})


@my_routes.route("/get_tweets")
def get_tweets():
    tweets = []
    client = twitter_api_client()
    statuses = client.user_timeline("elonmusk", tweet_mode="extended")
    for status in statuses:
        tweets.append({"id": status.id_str, "message": status.full_text})
    print(tweets)
    return jsonify({"message": "OK"})
