from pymongo import MongoClient
import secrets
import traceback
from auth import mongo_auth

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'local'
COLLECTION_NAME = 'tbl_universal'

def key_gen():

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection['db_autentic']['tbl_user']
    resp = None
    
    try:
        conn = MongoClient()
        resp = print("Conectado com sucesso para gerar uma key!!!")
    except Exception:
        resp = traceback.print_exc()
        print("Falha na conexão para registrar a keygen!!!")
    try:
        str_Key = secrets.token_urlsafe()
        rec_1 = collection.insert_one({"key": str_Key,
                                   "permit_expired": "",
                                   "permit_insert": True,
                                   "permit_update": True,
                                   "permit_delete": True,
                                   "permit_search": True})
        resp = {"key": str_Key}
    except Exception:
        resp = traceback.print_exc()

    connection.close()
    return resp

def insert_one(data):

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)

    if auth == True:
        try:
            conn = MongoClient()
            print("Conectado com sucesso para inserção!!")
        except Exception:
            resp = traceback.print_exc()

        try:
            rec_1 = collection.insert_one(data[1])
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = {"resut": "chave invalida"}

    connection.close()
    return resp

