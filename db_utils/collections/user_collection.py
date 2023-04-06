from db_utils.collections.collection import Collection
from bson import ObjectId, DBRef


class UserCollection(Collection):
    def __init__(self, db):
        super().__init__("users", db=db)

    def add_user(self, user):
        user_id = self.collection.insert_one(user).inserted_id
        return user_id

    def add_plant_to_user(self, user_id, plant):
        self.collection.update_one({"_id": user_id}, {"$push": {"plants": plant}})
        return True

    def get_users(self):
        users = self.collection.find({})
        return users

    def get_user(self, username=None, user_id=None, deref=False):
        if username:
            user = self.collection.find_one({"username": username})
        elif user_id:
            user_id = ObjectId(user_id)
            user = self.collection.find_one({"_id": user_id})
        else:
            raise ValueError("Must provide either username or user_id")

        if user:
            if "plants" in user and user["plants"] and deref:
                print(user["plants"])
                user["plants"] = [self.db.dereference(i) for i in user["plants"]]
                for i in user["plants"]:
                    i["species"] = self.db.dereference(i["species"])

        return user

    def add_plant_to_user(self, user_id, plant_id):
        user_id = ObjectId(user_id)
        plant_id = ObjectId(plant_id)
        self.collection.update_one(
            {"_id": user_id}, {"$push": {"plants": DBRef("user_plants", plant_id)}}
        )
        return plant_id
