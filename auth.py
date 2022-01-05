from pymongo import MongoClient
import traceback

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'local'
COLLECTION_NAME = 'tbl_user'

def mongo_auth(data):

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection['db_autentic']['tbl_user']
    resp = None
    
    try:
        resp =  collection.find_one({"key" : data[0]['key']})
        if resp:
            resp = True
        else:
            resp = "chave não existe"
    except Exception:
        resp = traceback.print_exc()

    connection.close()
    return resp