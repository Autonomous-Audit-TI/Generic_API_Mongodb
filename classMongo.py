from os import close
from pymongo import MongoClient
from datetime import date, datetime
import secrets
import traceback
from auth import mongo_auth
from mongo_conn import open_conection, close_conection

adminKey = "IgUJRhIIO@qdzBHS68udS#Omlz*jclBbosN$S4uUQZbGT#G16p"

# checks if the table name exists for the user
def check_table_exists(conn, tableName):
    database = conn['db_mongo']
    if tableName in database.list_collection_names():
        return True
    return False

#checks if the key provided is an admin key
def check_admin_key(key):
    if key == adminKey:
        return True
    return False

# dumps the previous data before 
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

def log_key_gen(data):
    connection = open_conection()
    collection = connection["db_mongo"]["log"]

    resp = None
    dateNow = datetime.now()
    dateNow = dateNow.date()
    try:
        collection.insert_one({ 
            "key" : data["key"], 
            "table_name" : data["table_name"], 
            "IP" : data["ip_addr"],
            "last_modified" : str(dateNow)
        })
        resp = { "result" : "OK" }
    except Exception:
        resp = traceback.print_exc()

    close_conection(connection)
    return resp

def key_gen(ip):

    connection = open_conection()
    collection = connection['db_autentic']['tbl_user']
    resp = None
    
    try:
        str_Key = secrets.token_urlsafe()
        collectionUsers = connection['db_mongo'][f"tbl_{str_Key}"]
        # print('i gen key', str_Key)
        collection.insert_one({"key": str_Key,
                                "permit_expired": "",
                                "permit_insert": True,
                                "permit_update": True,
                                "permit_delete": True,
                                "permit_search": True})
        collectionUsers.insert_one({"key": str_Key,
                                "permit_expired": "",
                                "permit_insert": True,
                                "permit_update": True,
                                "permit_delete": True,
                                "permit_search": True})
        log_key_gen({ "key" : str_Key, "table_name" : f"tbl_{str_Key}", "ip_addr" : ip })
        resp = {"key": str_Key, "table_name": f"tbl_{str_Key}"}
        print(resp)
    except Exception:
        resp = traceback.print_exc()

    close_conection(connection)
    return resp

def list_database_names(data):

    connection = open_conection()
    resp = None
    list = []
    auth = mongo_auth(data)
    # tableExists = check_table_exists(connection, f"tbl_{data[0]['key']}")
    isAdmin = check_admin_key(data[0]['key'])

    if auth == True and isAdmin:
        try:
            d = dict((db, [collection for collection in connection[db].list_collection_names()])
                for db in connection.list_database_names())
            resp = d
   
        except Exception:
            resp = traceback.print_exc()
    else:
        if auth == "chave não existe":
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        # elif tableExists:
        #     resp = {"message" : f"Key {data[0]['key']} does not exist"}
        else:
            resp = {"message" : f"Table tbl_{data[0]['key']} does not exist"}
        # resp = auth

    close_conection(connection)
    return str(resp)

def insert_one(data):

    dump_log("Insert",data)

    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)
    tableExists = check_table_exists(connection, data[0]['table_name'])
    isAdmin = check_admin_key(data[0]['key'])

    if auth == True and tableExists == True or isAdmin:
        try:
            rec_1 = collection.insert_one(data[1])
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        if auth == "chave não existe":
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        elif tableExists:
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        else:
            resp = {"message" : f"Table tbl_{data[0]['key']} does not exist"}


    close_conection(connection)
    return resp

def delete_one(data):
    dump_log("Delete",data)
    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)
    tableExists = check_table_exists(connection, data[0]['table_name'])
    isAdmin = check_admin_key(data[0]['key'])

    if auth == True and tableExists == True or isAdmin:
        try:
            myquery = { data[0]['col_name']: data[1]['word']} 
            print(myquery)
            collection.delete_one(myquery)
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        if auth == "chave não existe":
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        elif tableExists:
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        else:
            resp = {"message" : f"Table tbl_{data[0]['key']} does not exist"}

    close_conection(connection)
    return resp


def find_like(data):
    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    list = []
    auth = mongo_auth(data)
    tableExists = check_table_exists(connection, data[0]['table_name'])
    isAdmin = check_admin_key(data[0]['key'])

    if auth == True and tableExists == True or isAdmin:
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
        if auth == "chave não existe":
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        elif tableExists:
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        else:
            resp = {"message" : f"Table tbl_{data[0]['key']} does not exist"}
        # resp = auth

    close_conection(connection)
    return str(resp)

def find_all(data):

    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    list = []
    auth = mongo_auth(data)
    tableExists = check_table_exists(connection, data[0]['table_name'])
    isAdmin = check_admin_key(data[0]['key'])

    if auth == True and tableExists == True or isAdmin:
        try:
            search = collection.find()
            for x in search:
                list.append(x)
            resp = list
        except Exception:
            resp = traceback.print_exc()
    else:
        if auth == "chave não existe":
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        elif tableExists:
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        else:
            resp = {"message" : f"Table tbl_{data[0]['key']} does not exist"}
        # resp = auth

    close_conection(connection)
    return str(resp)


def update_one(data):
    connection = open_conection()
    collection = connection['db_mongo'][data[0]['table_name']]
    resp = None
    auth = mongo_auth(data)
    tableExists = check_table_exists(connection, data[0]['table_name'])
    isAdmin = check_admin_key(data[0]['key'])

    if auth == True and tableExists == True or isAdmin:
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
        if auth == "chave não existe":
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        elif tableExists:
            resp = {"message" : f"Key {data[0]['key']} does not exist"}
        else:
            resp = {"message" : f"Table tbl_{data[0]['key']} does not exist"}
        # resp = auth

    close_conection(connection)
    return resp
