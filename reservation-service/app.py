from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

from common.errors import BadRequest, NotFound

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://mongodb:27017/reservations'
mongo = PyMongo(app)


@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = list(mongo.db.reservations.find({}, {'_id': False}))
    return jsonify(reservations)


@app.route('/reservations/<id>', methods=['GET'])
def get_reservation(id):
    reservation = mongo.db.reservations.find_one(
        {'_id': ObjectId(id)}, {'_id': False})
    if not reservation:
        raise NotFound(f"Reservation not found with id {id}")
    return jsonify(reservation)


@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    required_fields = ['name', 'date']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")
    name = data['name']
    date_str = data['date']
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise BadRequest("Invalid date format, should be 'YYYY-MM-DD'")

    reservation = {
        'name': name,
        'date': date
    }
    result = mongo.db.reservations.insert_one(reservation)
    reservation['_id'] = str(result.inserted_id)
    return jsonify(reservation)


@app.route('/reservations/<id>', methods=['PUT'])
def update_reservation(id):
    data = request.json
    reservation = mongo.db.reservations.find_one({'_id': ObjectId(id)})
    if not reservation:
        raise NotFound(f"Reservation not found with id {id}")
    if 'name' in data:
        reservation['name'] = data['name']
    if 'date' in data:
        date_str = data['date']
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise BadRequest("Invalid date format, should be 'YYYY-MM-DD'")
        reservation['date'] = date
    mongo.db.reservations.replace_one({'_id': ObjectId(id)}, reservation)
    reservation['_id'] = str(reservation['_id'])
    return jsonify(reservation)


@app.route('/reservations/<id>', methods=['DELETE'])
def delete_reservation(id):
    result = mongo.db.reservations.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        raise NotFound(f"Reservation not found with id {id}")
    return "", 204


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
