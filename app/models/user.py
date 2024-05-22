class User:
    def __init__(self, db):
        self.collection = db["users"]

    def create_user(self, user_data):
        return self.collection.insert_one(user_data)

    def find_user_by_email(self, email):
        return self.collection.find_one({"email": email})

    def update_user(self, email, update_data):
        return self.collection.update_one({"email": email}, {"$set": update_data})

    def delete_user(self, user_id):
        return self.collection.delete_one({"_id": user_id})

    def get_all_users(self):
        return self.collection.find()

    def get_user_by_id(self, user_id):
        return self.collection.find_one({"_id": user_id})
