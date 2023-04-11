from db_utils.db import db
from bson import ObjectId, DBRef


class PlantSpecies:
    @staticmethod
    def get_all_species(db=db):
        plants = db.plant_species.find({})
        return plants

    def __init__(self, name, watering, light, ph, _id=None) -> None:
        self.name = name
        self.watering = watering
        self.light = light
        self.ph = ph

    def save(self, db=db):
        species_id = db.plant_species.insert_one(self.__dict__).inserted_id
        return species_id

    @staticmethod
    def find_plant_species_by_id(species_id, db=db):
        species_id = ObjectId(species_id)
        species = db.plant_species.find_one({"_id": species_id})
        return PlantSpecies(**species)

    @staticmethod
    def find_plant_species_by_name(name, db=db):
        species = db.plant_species.find_one({"name": name})
        return PlantSpecies(**species)


class Plant:
    def __init__(
        self,
        name,
        species,
        owner,
        watering_frequency=None,
        _id=None,
    ):
        self.name = name
        self.species = species
        self.watering_frequency = None
        self.owner = owner
        self.watering_frequency = watering_frequency
        if _id:
            self._id = _id

    def save(self, db=db):  # kind of chaos, would like to tidy up
        plant = self.__dict__
        plant["species"] = DBRef("plant_species", ObjectId(plant["species"]))
        plant["watering_frequency"] = db.dereference(plant["species"])["watering"]
        owner_id = plant["owner"]
        plant["owner"] = DBRef("users", ObjectId(plant["owner"]))

        plant_id = db.user_plants.insert_one(self.__dict__).inserted_id
        db.users.update_one(
            {"_id": ObjectId(owner_id)},
            {"$push": {"plants": DBRef("user_plants", ObjectId(plant_id))}},
        )
        self._id = plant_id

    def update(self, db=db):
        db.user_plants.update_one({"_id": self._id}, {"$set": self.__dict__})

    @staticmethod
    def find_plant_by_id(plant_id, db=db, deref=False):
        plant_id = ObjectId(plant_id)
        plant = (db.user_plants.find_one({"_id": plant_id}),)
        if deref:
            plant["owner"] = db.dereference(plant["owner"])
            plant["species"] = PlantSpecies(**db.dereference(plant["species"]))

        return Plant(**plant)
