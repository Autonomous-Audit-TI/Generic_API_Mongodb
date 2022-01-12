from flask import Flask, jsonify, request
from classMongo import insert_one, key_gen, find_like, list_database_names, delete_one, find_all, update_one

app = Flask(__name__)

@app.route('/', methods=['GET'])
def logo_print():

  with open('logo.txt') as f:
    lines = f.readlines()
  return jsonify(lines)
  
@app.route('/mongo_login', methods=['POST'])
def mongo_login():

    str_IP = request.remote_addr
    access_key = request.get_json()
    resp = key_gen(str_IP, access_key)
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
