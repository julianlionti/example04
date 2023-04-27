from flask import Flask, jsonify, request
import requests
import json

from common.errors import BadRequest, NotFound

app = Flask(__name__)

USER_SERVICE_URL = 'http://user-service:5001'
RESERVATION_SERVICE_URL = 'http://reservation-service:5002'


@app.route('/users', methods=['GET'])
def get_users():
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        if status_code == 400:
            raise BadRequest('Invalid query parameter')
        elif status_code == 404:
            raise NotFound('Users not found')
        else:
            raise


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        response = requests.get(f'{USER_SERVICE_URL}/users/{id}')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        if status_code == 404:
            raise NotFound(f"User not found with id {id}")
        else:
            raise


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        response = requests.post(f'{USER_SERVICE_URL}/users', json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        if status_code == 400:
            raise BadRequest('Missing required field')
        else:
            raise


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    try:
        response = requests.put(f'{USER_SERVICE_URL}/users/{id}', json=data)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        if status_code == 404:
            raise NotFound(f"User not found with id {id}")
        elif status_code == 400:
            raise BadRequest('Missing required field')
        else:
            raise


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        response = requests.delete(f'{USER_SERVICE_URL}/users/{id}')
        response.raise_for_status()
        return "", 204
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        if status_code == 404:
            raise NotFound(f"User not found with id {id}")
        else:
            raise


@app.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        response = requests.get(f'{RESERVATION_SERVICE_URL}/reservations')
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code
        if status_code == 404:
            raise NotFound('Reservations not found')
        else:
            raise


@app.route('/reservations/<id>', methods=['GET'])
def get_reservation(id):
    # Get reservation by id from the reservation service
    reservation_service_url = f"{RESERVATION_SERVICE_URL}/reservations/{id}"
    reservation_response = requests.get(reservation_service_url)

    # Check if the reservation exists
    if reservation_response.status_code == 404:
        raise NotFound(f"Reservation not found with id {id}")
    reservation_data = reservation_response.json()

    # Get user by name from the user service
    user_service_url = f"{USER_SERVICE_URL}/users?name={reservation_data['name']}"
    user_response = requests.get(user_service_url)
    if user_response.status_code == 404:
        raise NotFound(f"User not found with name {reservation_data['name']}")
    user_data = user_response.json()[0]

    # Combine reservation and user data
    response_data = {
        'id': id,
        'name': user_data['name'],
        'email': user_data['email'],
        'date': reservation_data['date']
    }

    return jsonify(response_data)


@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    url = f'{RESERVATION_SERVICE_URL}/users/{data["user_id"]}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise BadRequest(f"Error checking user: {str(e)}")
    reservation_data = {
        'name': data['name'],
        'date': data['date']
    }
    reservation_url = f'{RESERVATION_SERVICE_URL}/reservations'
    try:
        response = requests.post(reservation_url, json=reservation_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise BadRequest(f"Error creating reservation: {str(e)}")
    reservation_id = response.json()['_id']
    return jsonify({'reservation_id': reservation_id}), 201


@app.route('/reservations/<id>', methods=['PUT'])
def update_reservation(id):
    data = request.json
    url = f'{RESERVATION_SERVICE_URL}/reservations/{id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise NotFound(f"Error checking reservation: {str(e)}")
    reservation_data = {}
    if 'name' in data:
        reservation_data['name'] = data['name']
    if 'date' in data:
        reservation_data['date'] = data['date']
    reservation_url = f'{RESERVATION_SERVICE_URL}/reservations/{id}'
    try:
        response = requests.put(reservation_url, json=reservation_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise BadRequest(f"Error updating reservation: {str(e)}")
    return "", 204


@app.route('/reservations/<id>', methods=['DELETE'])
def delete_reservation(id):
    url = f'{RESERVATION_SERVICE_URL}/reservations/{id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise NotFound(f"Error checking reservation: {str(e)}")
    reservation_url = f'{RESERVATION_SERVICE_URL}/reservations/{id}'
    try:
        response = requests.delete(reservation_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise BadRequest(f"Error deleting reservation: {str(e)}")
    return "", 204


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
