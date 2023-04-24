from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from classes.user import User
from bson.json_util import dumps
from json import loads
from werkzeug.security import check_password_hash, generate_password_hash

user_app = Blueprint("user_app", __name__, template_folder="templates")


@user_app.route("/signup", methods=["GET", "POST"])
def singup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        if User.find_by_username(username):
            return render_template("signup.html", error="Username already exists")

        user = User(username=username, password=password, email=email)
        user.save()

        return redirect(url_for("login"))
    return render_template("signup.html")


@user_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.find_by_username(username)

        if not user:
            return render_template("login.html", error="Invalid username or password")

        if not check_password_hash(user.password, password):
            return render_template("login.html", error="Invalid username or password")

        session["user_id"] = str(user._id)
        session["username"] = user.username

        return redirect(url_for("user_app.profile", username=username))

    return render_template("login.html")


@user_app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("home"))


@user_app.route("/users")
def users():
    users = User.get_all_users()
    return render_template("users.html", users=users)


@user_app.route("/profile/<username>")
def profile(username):
    user = User.find_by_username(username, deref=True)

    if "user_id" in session and str(user._id) == session["user_id"]:
        print(user._id, session["user_id"])
        return render_template("my_profile.html", user=user)
    else:
        return render_template("profile.html", user=user)


@user_app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form["searchTerm"]
        search_results = User.search_users(search_term)
        return jsonify(loads(dumps(search_results)))

    elif request.method == "GET":
        search_term = request.args.get("searchTerm")
        search_results = list(User.search_users(search_term))
        print(search_results)
        return render_template(
            "search.html", search_results=search_results, search_term=search_term
        )
