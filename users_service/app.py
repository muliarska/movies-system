import re
from flask import Flask, request
from flask import make_response, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import abort


app = Flask(__name__)


# User API endpoint
API_PATH = '/movies_api'
SIGN_IN = API_PATH + '/sign_in'
SIGN_UP = API_PATH + '/sign_up'
USER_PROFILE = API_PATH + '/profile/<username>'
UPDATE_PROFILE = API_PATH + '/update_profile/<username>'
CHANGE_PASSWORD = API_PATH + '/change_password/<username>'
DELETE_ACCOUNT = API_PATH + '/delete_account/<username>'


error_pwd_validation_msg = 'Password must contain at least 6 characters, ' + \
                           'including Upper/Lowercase, special characters and numbers'


# To store users data
users_info = dict()
# TODO: Add database support.


# Fetches user profile details based on the username
@app.route(USER_PROFILE, methods=['GET'])
def user_profile(username):
    user = users_info[username]
    return make_response(jsonify({
        'name': user["name"],
        'email': user["email"],
        'dob': user["dob"]
    }), 200)


# User can update their user profile based on their username
@app.route(UPDATE_PROFILE, methods=['PUT'])
def update_profile(username):
    user = users_info[username]

    if 'name' in request.json:
        user["name"] = request.json['name']

    if 'email' in request.json:
        user["email"] = request.json['email']

    if 'dob' in request.json:
        user["dob"] = request.json['dob']

    return make_response(jsonify({
        'success': 'User profile updated successfully'
    }), 200)


# User can change password based on their username
@app.route(CHANGE_PASSWORD, methods=['PUT'])
def change_password(username):
    if 'old_password' in request.json and 'new_password' in request.json:
        user = users_info[username]

        old_password = request.json['old_password']
        new_password = request.json['new_password']

        if old_password == user["password"]:
            if password_validation(new_password) is None:
                return make_response(jsonify({"password_validation": error_pwd_validation_msg}), 400)
            user["password"] = new_password
        else:
            return make_response(jsonify({'success': "Old password doesn't matched with the current password"}), 200)
        return make_response(jsonify({'success': 'Password changed successfully'}), 200)
    else:
        return make_response(jsonify({'error': 'Missing Fields'}), 400)


# User can delete their account based on their username
@app.route(DELETE_ACCOUNT, methods=['DELETE'])
def delete_account(username):
    # Abort if there are no such username
    if username not in users_info:
        abort(404)

    del users_info[username]
    return make_response(jsonify({
        "success": 'Account Deleted Successfully'
    }), 200)


# User authentication as per their credentials
@app.route(SIGN_IN, methods=['POST'])
def sign_in():
    username = request.json['username']
    password = request.json['password']

    if username in users_info:
        user = users_info[username]
    else:
        return make_response(jsonify({
            'error': 'Incorrect Username'
        }), 401)

    if password == user["password"]:
        access_token = create_access_token(identity=username)

        return make_response(jsonify({
            'access_token': access_token,
            'name': user["name"],
            'email': user["email"],
            'dob': user["dob"]
        }), 200)
    else:
        return make_response(jsonify({
            'error': 'Incorrect Password'
        }), 401)


# Create new account with the user details
@app.route(SIGN_UP, methods=['POST'])
def sign_up():
    username = request.json['username']
    if username in users_info:
        return make_response(jsonify({"username": username+' username already exists'}), 400)
    else:
        pass

    email = request.json['email']
    if email_validation(email) is None:
        return make_response(jsonify({"email_validation": email+' is not a valid email address'}), 400)

    password = request.json['password']
    if password_validation(password) is None:
        return make_response(jsonify({"password_validation": error_pwd_validation_msg}), 400)

    users_info[username] = {"password": password,
                            "name": request.json['name'],
                            "email": email,
                            "dob": request.json['dob']
                            }

    return make_response(jsonify({
        "success": 'User Created Successfully'
    }), 201)


# Utility method to validate the password
def password_validation(password):
    pwd_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pwd_pattern = re.compile(pwd_regex)
    password_regex_match = re.search(pwd_pattern, password)
    return password_regex_match


# Utility method to validate the email address
def email_validation(email):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email_pattern = re.compile(email_regex)
    email_regex_match = re.search(email_pattern, email)
    return email_regex_match


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
