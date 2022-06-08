from flask import Flask, request, make_response, jsonify
import variables as var
from postgres_client import PostgresClient
import requests
import uuid
import utils


app = Flask(__name__)

postgres_client = PostgresClient(var.HOST, var.PORT, var.DB_NAME, var.PASSWORD, var.USER)
postgres_client.connect()


@app.route(var.USER_PROFILE, methods=['GET'])
def user_profile(username):
    if not utils.login_validation(username, postgres_client):
        return make_response(jsonify({
            'error': 'Incorrect username or not logged in user'
        }), 401)
    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)
    return make_response(jsonify({
        'name': user[0][3],
        'email': user[0][4],
        'dob': user[0][5]
    }), 200)


@app.route(var.UPDATE_PROFILE, methods=['PUT'])
def update_profile(username):
    if not utils.login_validation(username, postgres_client):
        return make_response(jsonify({
            'error': 'Incorrect username or not logged in user'
        }), 401)
    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)

    if 'name' in request.json:
        postgres_client.update_record(user[0][0], "name", request.json['name'], var.TABLE_NAME)

    if 'email' in request.json:
        postgres_client.update_record(user[0][0], "email", request.json['email'], var.TABLE_NAME)

    if 'dob' in request.json:
        postgres_client.update_record(user[0][0], "dob", request.json['dob'], var.TABLE_NAME)

    return make_response(jsonify({
        'success': 'User profile updated successfully'
    }), 200)


@app.route(var.CHANGE_PASSWORD, methods=['PUT'])
def change_password(username):
    if 'old_password' in request.json and 'new_password' in request.json:
        if not utils.login_validation(username, postgres_client):
            return make_response(jsonify({
                'error': 'Incorrect username or not logged in user'
            }), 401)
        user = postgres_client.select_user_by_username(username, var.TABLE_NAME)

        old_password = request.json['old_password']
        new_password = request.json['new_password']

        if old_password == user[0][2]:
            if utils.password_validation(new_password) is None:
                return make_response(jsonify({"password_validation": var.error_pwd_validation_msg}), 400)
            postgres_client.update_record(user[0][0], 'password', new_password, var.TABLE_NAME)
        else:
            return make_response(jsonify({'success': "Old password doesn't match with the current password"}), 200)
        return make_response(jsonify({'success': 'Password changed successfully'}), 200)
    else:
        return make_response(jsonify({'error': 'Missing Fields'}), 400)


@app.route(var.DELETE_ACCOUNT, methods=['DELETE'])
def delete_account(username):
    # Abort if there are no such username
    if not utils.login_validation(username, postgres_client):
        return make_response(jsonify({
            'error': 'Incorrect username or not logged in user'
        }), 401)
    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)
    if not user:
        return make_response(jsonify({
            "failure": 'Such user does not exist'
        }), 404)
    if request.json['password'] == user[0][2]:
        postgres_client.delete_record(user[0][0], var.TABLE_NAME)
        return make_response(jsonify({
            "success": 'Account Deleted Successfully'
        }), 200)
    else:
        return make_response(jsonify({
            "failure": 'Authentication failed'
        }), 404)


# User authentication as per their credentials
@app.route(var.LOG_IN, methods=['POST'])
def log_in():
    username = request.json['username']
    password = request.json['password']

    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)

    if not user:
        return make_response(jsonify({
            'error': 'User needs to sign up first'
        }), 401)

    if password == user[0][2]:

        postgres_client.update_record(user[0][0], 'log_in', True, var.TABLE_NAME)
        return make_response(jsonify({
            'name': user[0][3],
            'email': user[0][4],
            'dob': user[0][5]
        }), 200)
    else:
        return make_response(jsonify({
            'error': 'Incorrect Password'
        }), 401)


@app.route(var.LOG_OUT, methods=['POST'])
def log_out():
    username = request.json['username']

    if not utils.login_validation(username, postgres_client):
        return make_response(jsonify({
            'error': 'Incorrect username or not logged in user'
        }), 401)
    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)
    postgres_client.update_record(user[0][0], 'log_in', False, var.TABLE_NAME)
    return make_response(jsonify({
        'success': "Logged out successfully"
    }), 200)


@app.route(var.CHECK_LOG_IN, methods=['POST'])
def check_log_in():
    username = request.json['username']
    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)
    if user:
        return make_response(jsonify({
            'log_in': user[0][6]
        }), 200)
    else:
        return make_response(jsonify({
            'error': 'Incorrect Username'
        }), 401)



# Create new account with the user details
@app.route(var.SIGN_UP, methods=['POST'])
def sign_up():
    username = request.json['username']

    check_user_existence = postgres_client.select_user_by_username(username, var.TABLE_NAME)
    if check_user_existence:
        return make_response(jsonify({"username": username+' username already exists'}), 400)
    else:
        pass

    email = request.json['email']
    if utils.email_validation(email) is None:
        return make_response(jsonify({"email_validation": email+' is not a valid email address'}), 400)

    password = request.json['password']
    if utils.password_validation(password) is None:
        return make_response(jsonify({"password_validation": var.error_pwd_validation_msg}), 400)

    user_id = str(uuid.uuid4())
    data_to_insert = (user_id, username, password, request.json['name'], email, request.json['dob'], False)
    postgres_client.insert_records(data_to_insert, var.TABLE_NAME)

    return make_response(jsonify({
        "success": 'User Created Successfully'
    }), 200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
