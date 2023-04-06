from pymongo import MongoClient
from db_utils.collections.plant_info_collection import PlantSpeciesCollection
from db_utils.collections.user_plants_collection import UserPlantCollection
from db_utils.collections.user_collection import UserCollection
from bson import ObjectId, DBRef


class DBManager:
    def __init__(
        self,
        db_name,
    ):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.plant = PlantSpeciesCollection(db=self.db)
        self.user = UserCollection(db=self.db)
        self.user_plants = UserPlantCollection(db=self.db)

    def add_user_plant(self, plant):
        # get data from plant reference

        plant["watering_frequency"] = self.plant.get_plant(plant_id=plant["species"])[
            "watering"
        ]

        print(plant["owner"])
        print(type(plant["owner"]))
        owner_id = plant["owner"]

        plant_id = self.user_plants.add_plant(plant)
        print(type(plant["owner"]))

        self.user.add_plant_to_user(owner_id, plant_id)
        return plant_id
