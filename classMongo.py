from pymongo import MongoClient
from flask import json, jsonify
import secrets
import traceback
from auth import mongo_auth

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'db_mongo'
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
        print('i gen key', str_Key)
        collection.insert_one({"key": str_Key,
                                "permit_expired": "",
                                "permit_insert": True,
                                "permit_update": True,
                                "permit_delete": True,
                                "permit_search": True})
        resp = {"key": str_Key}
        print(resp)
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

def delete_one(data):

    # sample input => [{ key: "6mgKmhUk10Vfc21UVhLjAF26Y8YAx2TgUjfbg5Os9wg" }, { Nome_Completo: "Alexandre Novaes Iosimura" }]
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME]['tbl_demonstracao']
    resp = None
    auth = mongo_auth(data)

    if auth == True:
        try:
            conn = MongoClient()
        except Exception:
            resp = traceback.print_exc()

        try:
            rec_1 = collection.delete_one(data[1])
            resp = {"resut": "OK"}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = {"resut": "chave invalida"}

    connection.close()
    return resp

def insert_client(data):

    # sample input => [{ key: "6mgKmhUk10Vfc21UVhLjAF26Y8YAx2TgUjfbg5Os9wg" }, { Nome_Completo: "Alexandre Novaes Iosimura", Telefon: ... }]
    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME]['tbl_clientes']
    resp = None
    auth = mongo_auth(data)

    if auth == True:
        try:
            conn = MongoClient()
        except Exception:
            resp = traceback.print_exc()

        try:
            rec_1 = collection.insert_one(data[1])
            resp = {"resut": "Client Added", "data": rec_1}
        except Exception:
            resp = traceback.print_exc()
    else:
        resp = {"resut": "chave invalida"}

    connection.close()
    return resp

def find_like(data):

    connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
    collection = connection[DB_NAME][data[0]['table_name']]
    resp = None
    list = []
    auth = mongo_auth(data)

    if auth == True:
        try:
            conn = MongoClient()
        except Exception:
            resp = traceback.print_exc()
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
        resp = {"resut": "chave invalida"}

    connection.close()
    return str(resp)