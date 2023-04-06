from db_utils.collections.collection import Collection
from bson import ObjectId, DBRef


class PlantSpeciesCollection(Collection):
    def __init__(self, db):
        super().__init__("plant_species", db=db)

    def add_plant(self, plant):
        plant_id = self.collection.insert_one(plant).inserted_id
        return plant_id

    def get_plant(self, plant_name=None, plant_id=None):
        if plant_id:
            plant_id = ObjectId(plant_id)
            plant = self.collection.find_one({"_id": plant_id})
            return plant
        elif plant_name:
            plant = self.collection.find_one({"name": plant_name})
        else:
            raise ValueError("Must provide either plant_name or plant_id")
        return plant

    def get_plants(self):
        plants = self.collection.find({})
        return plants
