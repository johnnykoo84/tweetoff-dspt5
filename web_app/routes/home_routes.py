# web_app/routes/home_routes.py

from flask import Blueprint, render_template

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def index():
    return render_template("prediction_form.html")


@home_routes.route("/hello")
def hello():
    x = 2 + 2
    return f"Hello World! {x}"


@home_routes.route("/about")
def about():
    return "About me"


@home_routes.route("/iris")
def iris():
    from sklearn.datasets import load_iris
    from sklearn.linear_model import LogisticRegression
    X, y = load_iris(return_X_y=True)
    clf = LogisticRegression(random_state=0, solver='lbfgs',
                             multi_class='multinomial').fit(X, y)
    result = str(clf.predict(X[:100, :]))
    print(result)
    return result
