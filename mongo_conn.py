from pymongo import MongoClient

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

def open_conection():

    try:
        connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
        print("Conectado com sucesso !!!")
    except Exception:
        connection = False
        print("Falha na conexão !!!")
    
    return connection

def close_conection(connection):
    connection.close()
