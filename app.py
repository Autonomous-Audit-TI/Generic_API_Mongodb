from flask import Flask, jsonify, request
<<<<<<< HEAD
from classMongo import delete_one, insert_client, insert_one, key_gen, find_like
=======
from classMongo import insert_one, key_gen, find_like, list_database_names, delete_one, find_all, update_one
>>>>>>> 05cbabd297da5c2f7ef5803aec4c2e2eca52ee02

app = Flask(__name__)

@app.route('/', methods=['GET'])
def logo_print():

  with open('logo.txt') as f:
    lines = f.readlines()
  return jsonify(lines)
  
@app.route('/mongo_login', methods=['GET'])
def mongo_login():

    resp = key_gen()
    return jsonify(resp)


@app.route('/mongo_insert_one', methods=['POST'])
def mongo_insert_one():

  data = request.get_json()
  resp = insert_one(data)
  return jsonify(resp)

@app.route('/mongo_delete_one', methods=['POST'])
def mongo_delete_one():

  data = request.get_json()
  resp = delete_one(data)
  return jsonify(resp)

@app.route('/mongo_search', methods=['POST'])
def mongo_search():

  data = request.get_json()
  resp = find_like(data)
  return resp

@app.route('/mongo_update', methods=['POST'])
def mongo_update_one():
  data = request.get_json()
  resp = update_one(data)
  return resp

@app.route('/mongo_find_all', methods=['POST'])
def mongo_find_all():

  data = request.get_json()
  resp = find_all(data)
  return resp
  
@app.route('/mongo_list_database_names', methods=['POST'])
def mongo_list_database_names():

  data = request.get_json()
  resp = list_database_names(data)
  return resp


if __name__ == '__main__':
    app.run(debug=True)
