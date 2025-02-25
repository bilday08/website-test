from pymongo import MongoClient

client = MongoClient("mongodb://192.168.1.87:27017/")
db = client['user_db']

users_collection = db['users']
art_collection = db['art_items']

def init_db():
    pass

def init_art_items():
    pass