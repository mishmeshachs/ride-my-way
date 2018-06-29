from V1.models import Ride, Request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from V1.auth import validate  # pragma: no cover
from V1 import app  # pragma: no cover
from flask import Blueprint,\
    jsonify, request, make_response  # pragma: no cover

ride_blueprint = Blueprint('ride', __name__)
users = []
logged_in_user = None

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECS'] = ['access']
jwt = JWTManager(app)
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''Black listing'''
    jti = decrypted_token['jti']
    return jti in blacklist


@ride_blueprint.route('/api/v1/rides', methods=['POST'])
@jwt_required
def create_ride():
    '''Ride creation route'''
    current_user = get_jwt_identity()
    data = request.get_json()
    category = data.get('category')
    pick_up = data.get('pick_up')
    drop_off = data.get('drop_off')
    date_time = data.get('date_time')
    price = data.get('price')
    dict_data = {
        'category': category, 'pick_up': pick_up,
        'drop_off': drop_off,
        'date_time': date_time, 'price': price}
    if validate.val_none(**dict_data):
        result = validate.val_none(**dict_data)
        return jsonify(result), 406
    if validate.empty(**dict_data):
        result = validate.empty(**dict_data)
        return jsonify(result), 406
    njaro = Ride.ride.items()
    existing_ride = {
        k: v for k, v in njaro if data['category'] == v['category']}

    if existing_ride:
        return jsonify(
            {"message": "Ride category already exists"})
    else:
        new_ride = Ride(
            category, pick_up, drop_off, date_time, price, current_user)
        new_ride.create_ride()
        response = {'message': 'Ride Successfully Created',
                    'Created by': current_user}
        return make_response(jsonify(response)), 201


@ride_blueprint.route('/api/v1/rides/<int:ride_id>', methods=['DELETE'])
@jwt_required
def delete_ride(ride_id):
    '''Route for deleting a ride'''
    current_user = get_jwt_identity()  # Current_user is username
    target_njaro = Ride.get_ride(ride_id)
    if target_njaro:
        if current_user == target_njaro['owner']:
            delete_njaro = Ride.delete_ride(ride_id)
            return make_response(jsonify(delete_njaro)), 200
        return jsonify(
            {'message': 'You cannot delete a ride that is not yours'}), 401
    return jsonify(
        {'message': 'Cannot Delete. Resourse Not Found'}), 404


@ride_blueprint.route('/api/v1/rides/<int:rides_id>', methods=['PUT'])
@jwt_required
def update_ride(ride_id):
    '''Route for updating a ride details'''
    current_user = get_jwt_identity()  # Current_user is username
    target_njaro = Ride.get_ride(ride_id)
    if target_njaro:
        if current_user == target_njaro['owner']:
            data = request.get_json()
            Ride.update_ride(ride_id, data)
            return jsonify(
                {'message': 'Successfully Updated'}), 201
        return jsonify(
            {'message': 'You cannot update a ride that is not yours'}), 401

    return jsonify(
        {'message': 'Cannot Update. Resource Not Found'}), 404


@ride_blueprint.route('/api/v1/rides', methods=['GET'])
@jwt_required
def get_rides():
    '''route to get all rides'''
    # If GET method
    rides = Ride.get_all_rides()
    return make_response(jsonify(rides)), 200


@ride_blueprint.route('/api/v1/rides/<int:ride_id>', methods=['GET'])
@jwt_required
def get_a_ride(ride_id):
    '''route to get a ride info'''
    target_ride = Ride.get_ride(ride_id)
    if target_ride:
        return make_response(jsonify(target_ride)), 200
    else:
        return jsonify(
            {'message': 'Resource Not Found'}), 404


@ride_blueprint.route('/api/v1/rides/<int:ride_id>/requests', methods=['POST'])
@jwt_required
def create_request(ride_id):
    '''Route to post a ride request'''
    current_user = get_jwt_identity()
    if request.method == 'POST':
        requester = current_user
        new_request = Request(requester)
        new_request.add_request()
        response = {
            'message': 'Request Posted',
            'Request by': current_user}
        return make_response(jsonify(response)), 201


@ride_blueprint.route('/api/v1/rides/requests', methods=['GET'])
@jwt_required
def get_request():
    '''Route to get a requets'''
    return make_response(
        jsonify(Request.get_all_requests())), 200
