from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'

mongo = PyMongo(app)

#this function for look get all books in mongodb
@app.route('/book', methods=['GET'])
def get_all_books():
	book = mongo.db.books 
	output = []
	for s in book.find():
		output.append({'name' : s['name'], 'title' : s['title'], 'category' : s['category']})
	return jsonify({'result' : output})

#this function for searching document by name on url
@app.route('/book/<name>', methods=['GET']) #input value di url
def get_one_book(name=None):
  book = mongo.db.books
  s = book.find_one({"name" : name})
  if s:
    output = {'name' : s['name'], 'title' : s['title'], 'category' : s['category']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

#this function for insert new document
@app.route('/book', methods=['POST'])
def add_book():
  book = mongo.db.books
  name = request.json['name']
  title = request.json['title']
  category = request.json['category']
  books_id = book.insert({'name': name,'title' : title, 'category': category})
  new_book = book.find_one({'_id': books_id })
  output = {'name' : new_book['name'], 'title' : new_book['title'], 'category' : new_book['category']}
  return jsonify({'result' : output})

#this function for update document
@app.route('/book/update', methods=['POST'])
def update_book():
    book = mongo.db.books
    name = request.json['name']
    title = request.json['title']
    category = request.json['category']
    books_id = book.update_one({'name':name},{'$set' : {'title':title, 'category' : category}})
    new_book = book.find({'name': name })
    #output = {'ids': new_star['ids'],'name' : new_star['name'], 'distance' : new_star['distance']}
    return jsonify({'result': new_book})


#this function for delete document
@app.route('/book/delete', methods=['POST'])
def delete_book():
  book = mongo.db.books
  name = request.json['name']
  books_id = book.delete_one({'name' : name})
  return jsonify({'result' : 'success'})


if __name__ == '__main__':
    app.run(debug=True)
