from pymongo import MongoClient
import secrets
import traceback
from auth import mongo_auth
from mongo_conn import open_conection, close_conection

def key_gen():

    connection = open_conection()
    collection = connection['db_autentic']['tbl_user']
    resp = None
    
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

    close_conection(connection)
    return resp

def list_database_names(data):

    connection = open_conection()
    resp = None
    list = []
    auth = mongo_auth(data)

    if auth == True:
        try:
            d = dict((db, [collection for collection in connection[db].list_collection_names()])
                for db in connection.list_database_names())
            resp = d
   
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return str(resp)

def insert_one(data):

    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)

    if auth == True:
        try:
            rec_1 = collection.insert_one(data[1])
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return resp

def delete_one(data):

    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)

    if auth == True:
        try:
            myquery = { data[0]['col_name']: data[1]['word']} 
            print(myquery)
            collection.delete_one(myquery)
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return resp


def find_like(data):

    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    list = []
    auth = mongo_auth(data)

    if auth == True:
        try:
            #AQUI NÃO ESTA FUNCIONANDO COM O LIKE. ACHO QUE É SINTAX INCORRETA /.* TEXTO .*/
            #myquery = { data[0]['col_name']: '/.*'+ data[1]['word'] +'.*/'}  
            myquery = { data[0]['col_name']: data[1]['word']} 
            print(myquery)  
            search = collection.find(myquery)
            for x in search:
                list.append(x)
            resp = list
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return str(resp)

def find_all(data):

    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    list = []
    auth = mongo_auth(data)

    if auth == True:
        try:
            search = collection.find()
            for x in search:
                list.append(x)
            resp = list
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return str(resp)