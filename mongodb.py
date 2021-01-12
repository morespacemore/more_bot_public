from pymongo import MongoClient
from settings import MONGODB_LINK

client = MongoClient(MONGODB_LINK)
db = client.more_bot
collection = db.collection

def db_send_compliment(compliment_text):
    db_compliment = {"compliment_text": compliment_text}
    collection.compliment.insert_one(db_compliment).inserted_id

def db_send_error(error_text):
    db_error = {"error_text": error_text}
    collection.error.insert_one(db_error).inserted_id

def db_get_compliment():
    compliment_list = []
    for db_compliment in collection.compliment.find():
        compliment_list.append(db_compliment["compliment_text"])
    return compliment_list
get_compliment = db_get_compliment()

def db_get_error():
    error_list = []
    for db_error in collection.error.find():
        error_list.append(db_error["error_text"])
    return error_list
get_error = db_get_error()
