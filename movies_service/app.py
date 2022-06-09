from datetime import datetime
from flask import Flask, request, redirect
from flask import make_response, jsonify
import variables as var
from cassandra_client import CassandraClient
import uuid
import requests
import json

app = Flask(__name__)

client_cassandra = CassandraClient(var.HOST, var.PORT, var.KEYSPACE)
client_cassandra.connect()


# Fetches list of movies based on trending which has (> 95%) users ratings
@app.route(var.TRENDING_NOW, methods=['GET'])
def trending_now(username):

    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)

    trending_movies = client_cassandra.get_trending_movies(username, var.TRENDING_TABLE_NAME)
    trending = dict()
    i = 1
    for row in trending_movies:
        trending[str(i)] = row
        i += 1
    return make_response(jsonify(trending), 200)


# Fetches list of movies based on username
@app.route(var.GET_MOVIES, methods=['GET'])
def movies(username):
    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)
    movies_all = client_cassandra.get_movies_data(username, var.MOVIES_TABLE_NAME)
    movies_ret = {"columns": var.MOVIES_COLUMNS}
    temp = {}
    i = 1
    for row in movies_all:
        temp[str(i)] = row
        i += 1
    movies_ret["rows"] = temp
    return make_response(jsonify(movies_ret), 200)


# User can search for movie based on the title
@app.route(var.SEARCH_MOVIE, methods=['GET'])
def search_movie(username, title):
    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)
    movie_by_title = client_cassandra.get_by_title(username, title, var.MOVIES_TABLE_NAME)
    if movie_by_title:
        movies_ret = {"columns": var.MOVIES_COLUMNS}
        temp = {}
        i = 1
        for row in movie_by_title:
            temp[str(i)] = row
            i += 1
        movies_ret["rows"] = temp
        return make_response(jsonify(movies_ret), 200)
    else:
        return make_response(jsonify({
            "failure": 'Failed to find Movie'
        }), 404)


# User can delete movie based on the title
@app.route(var.DELETE_MOVIE, methods=['DELETE'])
def delete_movie(username, title):

    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)

    movie_movie_table = client_cassandra.get_by_title(username, title, var.MOVIES_TABLE_NAME)
    fv_movie = client_cassandra.get_by_title(username, title, var.FAVOURITES_TABLE_NAME)
    if fv_movie:
        tables = [var.MOVIES_TABLE_NAME, var.FAVOURITES_TABLE_NAME]
        ids = [movie_movie_table[0][0], fv_movie[0][0]]
        client_cassandra.delete_movie(ids, tables)
    elif movie_movie_table:
        tables = [var.MOVIES_TABLE_NAME]
        ids = [movie_movie_table[0][0]]
        client_cassandra.delete_movie(ids, tables)
    else:
        return make_response(jsonify({
            "failure": 'Failed to Delete Movie'
        }), 404)

    return make_response(jsonify({
        "success": 'Movie Deleted Successfully'
    }), 200)


# User can add/remove movies as per their favourites
@app.route(var.ADD_TO_FAVOURITE, methods=['PUT'])
def add_to_favourite(username, title):

    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)

    movie = client_cassandra.get_by_title(username, title, var.MOVIES_TABLE_NAME)
    if movie:
        current_time = datetime.now()
        id = str(uuid.uuid4())
        movies_favourites_data = (id, username, movie[0][2], True, current_time, current_time)
        client_cassandra.insert_favourite_movies_data(movies_favourites_data, var.FAVOURITES_TABLE_NAME)
    else:
        return make_response(jsonify({
            "failure": "Failed to add movie to favourite"
        }), 404)

    return make_response(jsonify({
            "success": "Add movies to favourites"
        }), 200)


# Fetches list of favourite movies based on the username
@app.route(var.FAVOURITE_MOVIES, methods=['GET'])
def favourite_movies(username):

    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                     headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)

    data_movies = client_cassandra.get_favourite_movies(username, var.FAVOURITES_TABLE_NAME)
    movies_dct = dict()
    i = 1
    for row in data_movies:
        print(row)
        movies_dct[str(i)] = row
        i += 1
    return make_response(jsonify(movies_dct), 200)


# User can add new movie into the database
@app.route(var.ADD_MOVIE, methods=['POST'])
def add_movie(username):
    data = {"username": username}
    response = requests.post(url=var.users_service_check_log_in, data=json.dumps(data),
                                 headers={"Content-Type": "application/json"})

    try:
        log_in = response.json()['log_in']
    except KeyError:
        return make_response(jsonify({
                        "failure": 'Such user does not exist'
                    }), 404)

    if not log_in:
        return make_response(jsonify({
                "failure": 'You are not logged in'
            }), 404)
    id = str(uuid.uuid4())
    current_time = datetime.now()
    movie = client_cassandra.get_by_username(username, var.MOVIES_TABLE_NAME)
    if movie:
        return make_response(jsonify({
                "success": 'Such movie was added earlier'
            }), 200)
    movies_data = (id, username, request.json['title'], request.json['movie_type'], request.json['ratings'],
                   request.json['duration'], request.json['age_restriction'], request.json['description'],
                   request.json['cast'], request.json['genres'], request.json['category'], request.json['production'],
                   request.json['country'], current_time, current_time)
    client_cassandra.insert_movies_data(movies_data, var.MOVIES_TABLE_NAME)

    id = str(uuid.uuid4())
    movies_ratings_data = (id, username, request.json['title'], request.json['ratings'], current_time, current_time)
    client_cassandra.insert_movies_ratings_data(movies_ratings_data, var.TRENDING_TABLE_NAME)

    if request.json['is_favourite'] is True:
        id = str(uuid.uuid4())
        favourite_movies_data = (id, username, request.json['title'], request.json['is_favourite'], current_time, current_time)
        client_cassandra.insert_favourite_movies_data(favourite_movies_data, var.FAVOURITES_TABLE_NAME)


    return make_response(jsonify({
        "success": 'Movie Added Successfully'
    }), 200)


@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Invalid Request ' + error}))


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Movie not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
