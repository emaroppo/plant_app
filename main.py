from flask import Flask, render_template, request, redirect, url_for, flash, session
from classes.plants import Plant, PlantSpecies
from bson import ObjectId, DBRef
from classes.user import User
from photo_upload.photo_app import photo_app
from plant.plant_app import plant_app
from user.user_app import user_app
from werkzeug.security import check_password_hash, generate_password_hash
import pickle

app = Flask(__name__, template_folder="templates", static_folder="static")
app.register_blueprint(photo_app, url_prefix="/upload")
app.register_blueprint(plant_app, url_prefix="/plant")
app.register_blueprint(user_app, url_prefix="/user")

with open("secret.pickle", "rb") as f:
    secret = pickle.load(f)

app.secret_key = secret


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
