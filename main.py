from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_utils.db_manager import DBManager
from classes.plants import Plant, PlantSpecies
from bson import ObjectId, DBRef
from classes.user import User
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
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


@app.route("/login", methods=["GET", "POST"])
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

        return redirect(url_for("profile", username=username))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("home"))


@app.route("/users")
def users():
    db = DBManager("plant_db")
    users = db.user.get_users()
    return render_template("users.html", users=users)


@app.route("/profile/<username>")
def profile(username):
    user = User.find_by_username(username, deref=True)
    species = PlantSpecies.get_all_species()

    if "user_id" in session and str(user._id) == session["user_id"]:
        print(user._id, session["user_id"])
        return render_template("my_profile.html", user=user, species=species)
    else:
        return render_template("profile.html", user=user, species=species)


@app.route("/create_plant", methods=["GET", "POST"])
def create_plant():
    if request.method == "POST":
        db = DBManager("plant_db")

        plant = dict()
        plant["name"] = request.form["plant_name"]
        plant["species"] = request.form["species"]
        plant["owner"] = request.form["user_id"]

        plant = Plant(**plant)
        plant.save()

        flash("Plant created successfully")

        return redirect(url_for("profile", username=request.form["username"]))


@app.route("/plant/<plant_id>")
def plant(plant_id):
    db = DBManager("plant_db")
    plant = db.user_plants.get_user_plant(plant_id, deref=True)
    return render_template("plant.html", plant=plant)


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
