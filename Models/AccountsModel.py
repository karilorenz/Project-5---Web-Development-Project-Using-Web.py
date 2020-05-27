import bcrypt
from pymongo import MongoClient


class RegisterModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codewiz
        self.Users = self.db.users

    def insert_user(self, data):
        hashed = bcrypt.hashpw(data.password.encode('utf8'), bcrypt.gensalt())

        id = self.Users.insert({"username": data.username, "name": data.name, "password": hashed, "email": data.email,
                                "avatar": "", "background": "", "about": "", "hobbies": "", "birthday": ""})
        print("uid is", id)


class LoginModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.codewiz
        self.Users = self.db.users

    def check_user(self, data):
        # Get user from Mongo database
        user = self.Users.find_one({"username": data.username})

        # Find user and password
        if user:
            if bcrypt.checkpw(data.password.encode('utf8'), user["password"]):
                return user
            else:
                return False
        else:
            return False

    def update_info(self, data):
        # Update info in pymongo
        updated = self.Users.update_one({
            "username": data["username"]
        }, {"$set": data})

        return True

    def get_profile(self, user):
        user_info = self.Users.find_one({"username": user})

        return user_info

    def update_image(self, update):
        updated = self.Users.update_one({"username": update["username"]},
                                        {"$set": {update["type"]: update["img"]}})

        return updated
