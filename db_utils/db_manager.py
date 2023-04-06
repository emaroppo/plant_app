from pymongo import MongoClient
from db_utils.collections.plant_collection import PlantSpeciesCollection
from db_utils.collections.user_collection import UserCollection


class DBManager:
    def __init__(
        self,
        db_name,
    ):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.plant = PlantSpeciesCollection(db=self.db)
        self.user = UserCollection(db=self.db)
