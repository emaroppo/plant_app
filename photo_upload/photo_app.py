from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from classes.user import User
from classes.plants import PlantSpecies, Plant
from datetime import datetime as dt
import os

photo_app = Blueprint("photo_app", __name__, template_folder="templates")

# upload profile picture
# save the file to /static/pics/usr/<user_id>/profile_picture.png
# save the path to the database


@photo_app.route("/upload_profile_picture", methods=["GET", "POST"])
def profile_picture():
    if request.method == "POST":
        user_id = session["user_id"]
        user = User.find_by_id(user_id)
        file = request.files["profile_picture_upload"]
        if not os.path.exists(f"./static/pics/usr/{user_id}"):
            os.makedirs(f"./static/pics/usr/{user_id}")
        file.save(f"./static/pics/usr/{user_id}/profile_picture.png")
        user.profile_picture = f"/static/pics/usr/{user_id}/profile_picture.png"
        user.update()
        return redirect(url_for("profile", username=user.username))


# upload plant picture
# save the file to /static/pics/usr/<user_id>/plants/<plant_id>/<plant_id>_<timestamp>.png
# save the path to the database


@photo_app.route("/plant_picture", methods=["GET", "POST"])
def plant_picture():
    if request.method == "POST":
        user_id = session["user_id"]
        user = User.find_by_id(user_id)
        plant_id = request.form["plant_id"]
        plant = Plant.find_by_id(plant_id)
        file = request.files["plant_picture_upload"]

        if not os.path.exists(f"./static/pics/usr/{user_id}/plants/{plant_id}/"):
            if not os.path.exists(f"./static/pics/usr/{user_id}/plants/"):
                if not os.path.exists(f"./static/pics/usr/{user_id}/"):
                    os.makedirs(f"./static/pics/usr/{user_id}/")
                os.makedirs(f"./static/pics/usr/{user_id}/plants/")
            os.makedirs(f"./static/pics/usr/{user_id}/plants/{plant_id}/")

        timestamp = int(dt.now().timestamp())

        file.save(
            f"./static/pics/usr/{user_id}/plants/{plant_id}/{plant_id}_{timestamp}.png"
        )
        plant.pictures.append(
            {
                "path": f"/static/pics/usr/{user_id}/plants/{plant_id}/{plant_id}_{timestamp}.png"
            }
        )
        plant.update()
        return redirect(url_for("profile", username=user.username))
    return render_template("upload_plant_picture.html")
