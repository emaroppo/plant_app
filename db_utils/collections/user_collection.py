from db_utils.collections.collection import Collection


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

    def get_user(self, username=None, user_id=None):
        if username:
            user = self.collection.find_one({"username": username})
            return user
        elif user_id:
            user = self.collection.find_one({"_id": user_id})
            return user
        else:
            raise ValueError("Must provide either username or user_id")
