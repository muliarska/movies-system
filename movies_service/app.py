from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import abort
from .database.models import Movies, get_movies, get_movie_by_title
from config import Config

movies_bp = Blueprint('movies', __name__)


def confirm_identity(username):
    if get_jwt_identity() != username:
        abort(401)
    return


# Fetches list of movies based on trending which has (> 95%) users ratings
@movies_bp.route(Config.TRENDING_NOW, methods=['GET'])
@jwt_required
def trending_now(username):
    confirm_identity(username)

    movies = get_movies()
    trending = []
    for movie in movies:
        # Checking if movie has more than 95% ratings
        if movie.ratings > 95:
            trending.append(movie)
    return make_response(jsonify(trending), 200)


# Fetches list of movies based on username
@movies_bp.route(Config.FETCH_MOVIES, methods=['GET'])
@jwt_required
def fetch_movies(username):
    confirm_identity(username)
    movies = get_movies()
    return make_response(jsonify(movies), 200)


# User can search for movie based on the title
@movies_bp.route(Config.SEARCH_MOVIE, methods=['GET'])
@jwt_required
def search_movie(username, title):
    confirm_identity(username)
    try:
        movie = get_movie_by_title(title=title)
        return make_response(jsonify(movie), 200)
    except Movies.DoesNotExist:
        abort(404)


# User can delete movie based on the title
@movies_bp.route(Config.DELETE_MOVIE, methods=['DELETE'])
@jwt_required
def delete_movie(username, title):
    confirm_identity(username)
    movie = get_movie_by_title(title=title)

    # Abort if no movie
    if movie is None:
        abort(404)

    movie.delete()
    return make_response(jsonify({
        "success": 'Movie Deleted Successfully'
    }), 200)


# User can add/remove movies as per their favourites
@movies_bp.route(Config.ADD_TO_FAVOURITE, methods=['PUT'])
@jwt_required
def add_to_favourite(username, title):
    confirm_identity(username)
    movie = get_movie_by_title(title=title)

    # Abort if no movie found
    if movie is None:
        abort(404)

    movie.update(is_favourite=request.json['is_favourite'])

    if request.json['is_favourite']:
        message = title + ' has been added to your favourite'
    else:
        message = title + ' has been removed from your favourite'

    return make_response(jsonify({
        "success": message
    }), 200)


# Fetches list of favourite movies based on the username
@movies_bp.route(Config.FAVOURITE_MOVIES, methods=['GET'])
@jwt_required
def favourite_movies(username):
    confirm_identity(username)
    movies = get_movie_by_title()
    return make_response(jsonify(movies), 200)


# User can add new movie into the database
@movies_bp.route(Config.ADD_MOVIE, methods=['POST'])
@jwt_required
def add_movie(username):
    confirm_identity(username)
    try:
        movies = Movies(title=request.json['title'],
                        movie_type=request.json['movie_type'],
                        ratings=request.json['ratings'],
                        duration=request.json['duration'],
                        age_restriction=request.json['age_restriction'],
                        timestamp=request.json['timestamp'],
                        thumbnails=request.json['thumbnails'],
                        media=request.json['media'],
                        subtitles=request.json['subtitles'],
                        description=request.json['description'],
                        cast=request.json['cast'],
                        genres=request.json['genres'],
                        category=request.json['category'],
                        production=request.json['production'],
                        country=request.json['country'],
                        is_favourite=request.json['is_favourite'])
        movies.save()
    except KeyError:
        abort(400)

    return make_response(jsonify({
        "success": 'Movies Added Successfully'
    }), 201)


@movies_bp.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'Invalid Request ' + error}))


@movies_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Movie not found'}), 404)


@movies_bp.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)
