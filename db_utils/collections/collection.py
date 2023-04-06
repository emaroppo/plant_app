class Collection:
    def __init__(self, collection_name, db):
        self.name = collection_name
        self.db = db
        self.collection = db[self.name]
