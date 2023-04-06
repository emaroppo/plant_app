from db_utils.collections.collection import Collection


class PlantSpeciesCollection(Collection):
    def __init__(self, db):
        super().__init__("plant_species", db=db)

    def add_plant(self, plant):
        plant_id = self.collection.insert_one(plant).inserted_id
        return plant_id

    def get_plant(self, plant_name):
        plant = self.collection.find_one({"name": plant_name})
        return plant
