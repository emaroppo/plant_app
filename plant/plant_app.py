from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from bson.json_util import dumps
from json import loads
from classes.plants import Plant, PlantSpecies

plant_app = Blueprint("plant_app", __name__, template_folder="templates")


@plant_app.route("/create_plant", methods=["GET", "POST"])
def create_plant():
    if request.method == "POST":
        plant = dict()
        plant["name"] = request.form["plant_name"]
        plant["species"] = request.form["species"]
        plant["owner"] = request.form["user_id"]

        plant = Plant(**plant)
        plant.save()

        flash("Plant created successfully")

        return redirect(url_for("user_app.profile", username=request.form["username"]))


@plant_app.route("/<plant_id>")
def plant(plant_id):
    plant = Plant.find_by_id(plant_id, deref=True)
    if str(plant.owner["_id"]) == session["user_id"]:
        return render_template("plant.html", plant=plant, owner=True)
    return render_template("plant.html", plant=plant, owner=False)


@plant_app.route("/list_species")
def list_species():
    return jsonify(loads(dumps(PlantSpecies.get_all_species())))
