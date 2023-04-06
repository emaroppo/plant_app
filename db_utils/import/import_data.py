# create mongo db containing plant data
import json
import pymongo
from pymongo import MongoClient
import os
import sys
import re
import time

# connect to mongo db
client = MongoClient()
db = client.plant_db
collection = db.plant_species

# open json file
with open("db_utils/plant.json") as data_file:
    data = json.load(data_file)
    count = 0
    loaded_plants = list(collection.find({}, {"name": 1}))
    loaded_plants = [i["name"] for i in loaded_plants]

    for i in data:
        i["name"] = i["name"].lower()
        if i["name"] not in loaded_plants:
            i["ph"] = {"min": i["ph"][0], "max": i["ph"][1]}
            plant_id = collection.insert_one(i).inserted_id
            print(f'Inserted {i["name"]}  with id {plant_id}')
            count += 1

    collection.create_index([("name", pymongo.ASCENDING)], unique=True)

    print(f"Inserted {count} new plants")
