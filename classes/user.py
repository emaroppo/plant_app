from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, DBRef
from db_utils.db import db


class User:
    @staticmethod
    def get_all_users():
        users = db.users.find({})
        return users

    @staticmethod
    def search_users(search_term):
        users = db.users.find({"username": {"$regex": search_term}})
        return users

    def __init__(self, username, password, email, _id=None, plants=[]):
        self._id = _id
        self.username = username
        self.email = email
        self.password = password
        self.plants = plants

    def save(self):
        user_id = db.users.insert_one(
            {
                "username": self.username,
                "password": generate_password_hash(self.password),
                "email": self.email,
            }
        ).inserted_id

        self._id = user_id

    def update(self):
        if not self._id:
            raise ValueError("User instance has not been saved to the database")
        update_data = vars(self)
        del update_data["_id"]  # remove _id from update data
        update_result = db.users.update_one({"_id": self._id}, {"$set": update_data})
        if update_result.matched_count == 0:
            raise ValueError("User instance not found in the database")

    @staticmethod
    def find_by_id(user_id, db=db, deref=False):
        user_id = ObjectId(user_id)
        user = db.users.find_one({"_id": user_id})
        if user:
            if "plants" in user and user["plants"] and deref:
                user["plants"] = [db.dereference(i) for i in user["plants"]]
                for i in user["plants"]:
                    i["species"] = db.dereference(i["species"])
            return User(**user)

    @staticmethod
    def find_by_username(username, db=db, deref=False):
        user = db.users.find_one({"username": username})
        if user:
            if "plants" in user and user["plants"] and deref:
                user["plants"] = [db.dereference(i) for i in user["plants"]]
                for i in user["plants"]:
                    i["species"] = db.dereference(i["species"])
            return User(**user)
