from flask import Flask, render_template, request, redirect, url_for, flash
from db_utils.db_manager import DBManager

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        db = DBManager("plant_db")
        user = db.user.get_user(username)
        if user:
            flash("Username already exists")
            return redirect(url_for("signup"))
        else:
            user = dict()
            user["username"] = username
            user["password"] = password
            user["email"] = email

            db.user.add_user(user)
            flash("User created successfully")
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = DBManager("plant_db")
        user = db.user.get_user(username)
        if user and user["password"] == password:
            flash("Login successful")
            return redirect(url_for("home"))
        else:
            flash("Incorrect credentials")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/users")
def users():
    db = DBManager("plant_db")
    users = db.user.get_users()
    return render_template("users.html", users=users)


@app.route("/profile/<username>")
def profile(username):
    db = DBManager("plant_db")
    user = db.user.get_user(username)
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
