from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

from common.errors import BadRequest, NotFound

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/users'
mongo = PyMongo(app)


@app.route('/users', methods=['GET'])
def get_users():
    users = list(mongo.db.users.find({}, {'_id': False}))
    return jsonify(users)


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)}, {'_id': False})
    if not user:
        raise NotFound(f"User not found with id {id}")
    return jsonify(user)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")
    name = data['name']
    email = data['email']
    user = {
        'name': name,
        'email': email
    }
    result = mongo.db.users.insert_one(user)
    user['_id'] = str(result.inserted_id)
    return jsonify(user)


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if not user:
        raise NotFound(f"User not found with id {id}")
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    mongo.db.users.replace_one({'_id': ObjectId(id)}, user)
    user['_id'] = str(user['_id'])
    return jsonify(user)


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        raise NotFound(f"User not found with id {id}")
    return "", 204


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
