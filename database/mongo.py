from pymongo import MongoClient
import config

def get_mongo_client():
    return MongoClient(config.MONGO_URI)

def get_database():
    client = get_mongo_client()
    return client["entertainment"]