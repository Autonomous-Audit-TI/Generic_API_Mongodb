from flask import Flask, jsonify, request
from classMongo import insert_one, key_gen


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


if __name__ == '__main__':
    app.run(debug=True)
