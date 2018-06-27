
from V1.models import User
import uuid
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from werkzeug.security import check_password_hash
from V1.auth import validate  # pragma: no cover
from V1 import app  # pragma: no cover
from flask import Blueprint,\
    jsonify, request, make_response  # pragma: no cover

auth_blueprint = Blueprint('auth', __name__)
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


@auth_blueprint.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    '''Route to register user'''
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    dict_data = {'email': email, 'username': username, 'password': password}
    if validate.val_none(**dict_data):
        result = validate.val_none(**dict_data)
        return jsonify(result), 406
    if validate.empty(**dict_data):
        result = validate.empty(**dict_data)
        return jsonify(result), 406
    val_pass = validate.whitespace(dict_data['username'])
    if val_pass:
        return jsonify(
            {'message': 'Username cannot contain white spaces'}), 406
    val_length = validate.pass_length(dict_data['password'])
    if val_length:
        return jsonify(
            {'message':
                'Password is weak! Must have atleast 8 characters'}), 406
    val_email = validate.email_prtn(email)
    if val_email:
        return jsonify(
            {'message':
                'Email format is user@example.com'}), 406

    person = User.users.items()
    existing_email = {k: v for k, v in person if data['email'] == v['email']}
    existing_username = {
        k: v for k, v in person if data['username'] == v['username']}

    if existing_email:
        return jsonify({'message': 'Email already existing.'}), 409

    elif existing_username:
        return jsonify({'message': 'Username already existing.'}), 409
    else:
        new_person = User(email, username, password)
        new_person.create_user()
        return jsonify({'message': 'User Succesfully Registered'}), 201


@auth_blueprint.route('/api/v1/auth/login', methods=['POST'])
def login():
    '''Route to login'''

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    dict_data = {'username': username, 'password': password}
    if validate.val_none(**dict_data):
        result = validate.val_none(**dict_data)
        return jsonify(result), 406
    if validate.empty(**dict_data):
        result = validate.empty(**dict_data)
        return jsonify(result), 406
    person = User.users.items()
    existing_user = {
        k: v for k, v in person if data['username'] == v['username']}
    if existing_user:
        valid_user = [v for v in existing_user.values()
                      if check_password_hash(v['password'], password)]
        if valid_user:
            access_token = create_access_token(
                identity=username)
            if access_token:
                response = {
                    'message': 'You are logged in successfully',
                    'access_token': access_token
                }
                return make_response(jsonify(response)), 200
        else:
            return jsonify({'message': 'Wrong password'}), 400
    else:
        return jsonify({'message': 'Non-existent user. Try signing up'}), 404


@auth_blueprint.route('/api/v1/auth/change_password', methods=['POST'])
@jwt_required
def change_password():
    '''Route to change password'''
    current_user = get_jwt_identity()
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    dict_data = {'old_password': old_password, 'new_password': new_password}
    if validate.val_none(**dict_data):
        result = validate.val_none(**dict_data)
        return jsonify(result), 406
    if validate.empty(**dict_data):
        result = validate.empty(**dict_data)
        return jsonify(result), 406
    val_length = validate.pass_length(dict_data['new_password'])
    if val_length:
        return jsonify(
            {'message':
                'Password is weak! Must have atleast 8 characters'}), 406
    person = User.users.items()
    existing_username = {
        k: v for k, v in person if current_user == v['username']}
    valid_user = [v for v in existing_username.values()
                  if check_password_hash(v['password'], old_password)]
    if valid_user:
        User.change_password(current_user, data)
        return jsonify({'message': 'Reset successful'}), 200
    else:
        return jsonify(
            {'message':
                'Wrong Password. Cannot reset. Forgotten password?'}), 401


@auth_blueprint.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required
def logout():
    '''Route to logut'''
    dump = get_raw_jwt()['jti']
    blacklist.add(dump)
    return jsonify({'message': 'Logout successful'}), 200
