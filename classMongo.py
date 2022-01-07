from pymongo import MongoClient
import secrets
import traceback
from auth import mongo_auth
from mongo_conn import open_conection, close_conection

def dump_log(sp,data):
    connection = open_conection()
    collection = connection['db_mongo']["log"]
    collection1 = connection['db_mongo'][data[0]['table_name']]

    resp = None
    auth = mongo_auth(data)

    if auth == True:
        try:
            arr=[]
            data=collection1.find()
            for x in data:
                arr.append(x)
            
            
            rec_1 = collection.insert_one({sp:arr})
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return resp



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

    dump_log("Insert",data)

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
    dump_log("Delete",data)
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
            ################################################################################
            # 04-01-2022 - Jean Guilherme
            # AQUI NÃO ESTA FUNCIONANDO COM O LIKE. ACHO QUE É SINTAX INCORRETA /.* TEXTO .*/
            #myquery = { data[0]['col_name']: '/.*'+ data[1]['word'] +'.*/'}
            
            #################################################################################
            #Alexandre Novaes Iosimura - Search using regex to support LIKE argument - Solved
            ##################################################################################
            #temp="/^"+data[1]['word']+"/" 
            # Troubleshooting after pip3 install bson : the application broke, then:
            # I think the reason is I install pymongo and then install bson. Then I uninstall bson. Then I got this problem.
            # pip freeze pymongo it requires Nothing.
            # So maybe it has its own bson package.
            # What I solve this problem:
            # pip uninstall pymongo
            # pip uninstall bson
            # and then reinstall pymongo
            # pip install pymongo
            ############ SOLVED ######################################
            # Lets get ahead: using Regex
            # # use $options:'i' to make the query case-insensitive
            # # Ref.: https://kb.objectrocket.com/mongo-db/how-to-query-mongodb-documents-with-regex-in-python-362
            # use $regex to find docs that start with case-sensitive letter "object"
            # Examples:
            # query = { "field": { "$regex": 'obje.*' } }
            # docs = col.count_documents( query )
            # print ("query:", query)
            # print ("$regex using '.___*' -- total:", docs, "\n")

            # # the query between the ^ and $ char are for finding exact matches
            # query = { "field": { "$regex": '^ObjectRocket 2$' } }
            # docs = col.count_documents( query )
            # print ("query:", query)
            # print ("$regex using '^___$' -- total:", docs, "\n")
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            
            myquery = { data[0]['col_name']: { "$regex": data[1]['word'], "$options" :'i' } }
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


def update_one(data):
    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)
    if auth == True:
        try:
            filter = { data[0]['col_name']: data[1]['word']}
            update = { "$set": {data[2]['key']:data[2]["new_value"]}} 
            print(filter)
            print(update)
            collection.update_one(filter,update)
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = auth

    close_conection(connection)
    return resp
