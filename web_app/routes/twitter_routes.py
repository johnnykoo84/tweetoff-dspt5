# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify, request
from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import api as twitter_api_client
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)


@twitter_routes.route("/users")
def get_users():
    db_users = User.query.all()
    print(db_users)

    users = parse_records(db_users)
    print("@@@@@@")
    print(users)
    result = []
    for user in users:
        print('user!!', user)
        result.append(user['screen_name'])
    print('result@@@@')
    print(result)
    return jsonify(result)


@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    twitter_user = twitter_api_client.get_user(screen_name)
    statuses = twitter_api_client.user_timeline(
        screen_name, tweet_mode="extended", count=150)
    print("STATUSES COUNT:", len(statuses))
    # return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    # return "OK"
    # breakpoint()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api_client().embed_sentences(
        all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id  # or db_user.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter += 1
    db.session.commit()
    # return "OK"
    # tweets=db_tweets
    return render_template("user.html", user=db_user, tweets=statuses)


# @book_routes.route("/books/create", methods=["POST"])
# def create_book():
#     print("FORM DATA:", dict(request.form))
#     # todo: store in database
#     # return jsonify({
#     #     "message": "BOOK CREATED OK (TODO)",
#     #     "book": dict(request.form)
#     # })
#     new_book = Book(title=request.form["title"],
#                     author_id=request.form["author_name"])

#     db.session.add(new_book)
#     db.session.commit()

#     # return jsonify({
#     #     "message": "BOOK CREATED OK",
#     #     "book": dict(request.form)
#     # })
#     flash(f"Book '{new_book.title}' created successfully!", "success")
#     return redirect(f"/books")

# @book_routes.route("/books/new")
# def new_book():
    # return render_template("new_book.html")

@twitter_routes.route("/users/new")
def new_user():
    return render_template("new_tweet_user.html")


@twitter_routes.route("/users/create", methods=["POST"])
def create_user():
    print("FORM DATA", dict(request.form))
    # return jsonify({
    #     "message": "it works!"
    # })
    new_user = User(
        screen_name=request.form["screen_name"]
    )
    screen_name = request.form["screen_name"]
    print(screen_name)

    twitter_user = twitter_api_client.get_user(screen_name)
    statuses = twitter_api_client.user_timeline(
        screen_name, tweet_mode="extended", count=150)
    print("STATUSES COUNT:", len(statuses))
    # return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    # return "OK"
    # breakpoint()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api_client().embed_sentences(
        all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id  # or db_user.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter += 1
    db.session.commit()
    # return "OK"
    # tweets=db_tweets
    return render_template("user.html", user=db_user, tweets=statuses)
