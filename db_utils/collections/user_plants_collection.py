from db_utils.collections.collection import Collection
from bson import ObjectId, DBRef


class UserPlantCollection(Collection):
    def __init__(self, db):
        super().__init__("user_plants", db)

    def add_plant(self, plant):
        plant["owner"] = DBRef("users", ObjectId(plant["owner"]))
        plant["species"] = DBRef("plant_species", ObjectId(plant["species"]))
        plant_id = self.collection.insert_one(plant).inserted_id
        return plant_id

    def get_user_plant(self, plant_id, deref=False):
        plant_id = ObjectId(plant_id)
        plant = self.collection.find_one({"_id": plant_id})
        if deref:
            plant["owner"] = self.db.dereference(plant["owner"])
            plant["species"] = self.db.dereference(plant["species"])
        return plant
