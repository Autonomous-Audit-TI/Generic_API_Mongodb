from flask import Flask, jsonify, request
from classMongo import delete_one, insert_client, insert_one, key_gen, find_like

app = Flask(__name__)

@app.route('/', methods=['GET'])
def logo_print():

  with open('logo.txt') as f:
    lines = f.readlines();
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

@app.route('/mongo_insert_client', methods=['POST'])
def mongo_insert_client():

  data = request.get_json()
  resp = insert_client(data)
  return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True)
