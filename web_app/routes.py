import pandas as pd
from flask import Blueprint, jsonify, request, render_template ,current_app
from web_app.models import User, Tweet, db
from web_app.twitter_service import twitter_api_client
from web_app.basilica_service import embed_tweets
from sklearn.ensemble import RandomForestClassifier


my_routes = Blueprint("my_routes", __name__)

#
# ROUTING
#
client = twitter_api_client()

@my_routes.route("/")
def index():
    # return "Hello World!"
    return render_template("homepage.html")


@my_routes.route("/about")
def about():
    return "About Me"


@my_routes.route("/users")
@my_routes.route("/users.json")
def users():
    # users = [
    #    {"id":1, "name": "First User"},
    #    {"id":2, "name": "Second User"},
    #    {"id":3, "name": "Third User"},
    # ]
    # return jsonify(users)

    users = User.query.all()  # returns a list of <class 'alchemy.User'>
    print(type(users))
    print(type(users[0]))
    # print(len(users))

    users_response = []
    for u in users:
        user_dict = u.__dict__
        del user_dict["_sa_instance_state"]
        users_response.append(user_dict)

    return jsonify(users_response)


@my_routes.route("/users/create", methods=["POST"])
def create_user():
    print("CREATING A NEW USER...")
    print("FORM DATA:", dict(request.form))
    # todo: create a new user
    # return jsonify({"message": "CREATED OK (TODO)"})
    if "username" in dict(request.form):
        name = request.form["username"]
        country = request.form["country"]
        db.session.add(User(name=name))
        # db.session.add(User(country=country))
        db.session.commit()
        return jsonify({"message": "CREATED OK", "name": name})
    else:
        return jsonify({"message": "OOPS PLEASE SPECIFY A NAME!"})

# GET /hello
# GET /hello?name=Polly
@my_routes.route("/hello")
def hello(name=None):
    print("VISITING THE HELLO PAGE")
    print("REQUEST PARAMS:", dict(request.args))

    if "name" in request.args:
        name = request.args["name"]
        message = f"Hello, {name}"
    else:
        message = "Hello World"

    # return message
    return render_template("hello.html", message=message)


@my_routes.route("/get_tweets")
def get_tweets():
    tweets = []

    statuses = client.user_timeline("elonmusk", tweet_mode="extended")
    for status in statuses:
        tweets.append({"id": status.id_str, "message": status.full_text})
    print(tweets)
    return jsonify(tweets)


@my_routes.route("/get_user_tweets")
def get_user_tweets():
    return render_template("user_tweets.html")


@my_routes.route("/user_tweets", methods=["POST"])
def user_tweets():
    tweets = []
    client = twitter_api_client()
    handle = dict(request.form)
    statuses = client.user_timeline(handle['username'], tweet_mode="extended")
    for status in statuses:
        tweets.append({"created": status.created_at,
                       "user": status.user,
                       "message": status.full_text})
    return render_template("user_timeline.html",
                           tweets=tweets,
                           handle=handle)


@my_routes.route("/predict_twitter_user")
def predict_twitter_user():
    return render_template("/predict_twitter_user.html")


@my_routes.route("/make_prediction", methods=["POST"])
def make_prediction():
    tweets_A = []
    tweets_B = []
    messages_A = []
    messages_B = []
    form_data = dict(request.form)
    statuses_A = client.user_timeline(form_data['username-a'],
                                      tweet_mode="extended")
    statuses_B = client.user_timeline(form_data['username-b'],
                                      tweet_mode="extended")
    for status in statuses_A:
        tweets_A.append({"message": status.full_text,
                         "user": status.user})
        messages_A.append(status.full_text)
    for status in statuses_B:
        tweets_B.append({"message": status.full_text,
                         "user": status.user})
        messages_B.append(status.full_text)
    embeds_A = embed_tweets(messages_A)
    embeds_B = embed_tweets(messages_B)

    # TODO:
    # 1. Need to get the embedded tweets and the associated user into a
    # pandas dataframe.
    # 2. Fit a RandomForestClassifier onto the dataframe
    # 3. Make a prediction
    # 4. return the probabilities as context variables (as seen in the
    # user_tweets route above).
    # 5. store everything in the database - including the specifics of each
    # prediction that gets made
    # 6. Make everything pretty with Bootstrap, and add template inheritance
