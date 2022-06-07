import dataclasses
from typing import List

from flask import Flask, request, redirect
from flask import make_response, jsonify
from werkzeug.exceptions import abort
from dataclasses import dataclass

app = Flask(__name__)

# Movies API endpoint
API_PATH = '/movies_api'
TRENDING_NOW = API_PATH + '/trending_now/<username>'
GET_MOVIES = API_PATH + '/movies/<username>'
ADD_MOVIE = API_PATH + '/add_movie/<username>'
SEARCH_MOVIE = API_PATH + '/search_movie/<title>/<username>'
DELETE_MOVIE = API_PATH + '/delete_movie/<title>/<username>'
ADD_TO_FAVOURITE = API_PATH + '/add_to_favourites/<title>/<username>'
FAVOURITE_MOVIES = API_PATH + '/favourite_movies/<username>'


# To store movies data
@dataclass
class Thumbnail:
    type: str
    client: str
    size: int
    path: str


@dataclass
class Media:
    type: str
    client: str
    path: str


@dataclass
class Subtitles:
    language: str
    path: str


@dataclass
class Movie:
    title: str
    movie_type: str
    ratings: int
    duration: int
    age_restriction: int
    timestamp: int
    thumbnails: List[Thumbnail]
    media: List[Media]
    subtitles: List[Subtitles]
    description: str
    cast: List[str]
    genres: List[str]
    category: str
    production: str
    country: str
    is_favourite: bool


# Example for query
thumbnail = Thumbnail(
    type='words',
    client='netflix',
    size=150,
    path='./thumbnails'
)

media = Media(
    type='short_video',
    client='netflix',
    path='./media'
)

subtitles = Subtitles(
    language='ukrainian',
    path='./subtitles'
)

movie = Movie(
    title='Harry Potter',
    movie_type='horror',
    ratings=98,
    duration=100,
    age_restriction=13,
    timestamp=1200,
    thumbnails=[thumbnail],
    media=[media],
    subtitles=[subtitles],
    description='...',
    cast=['John Doe'],
    genres=['horror', 'comedy', 'family'],
    category='horror',
    production='Britain Entertainment',
    country='Britain',
    is_favourite=True,
)

# movies_info = {_movie_title: Movie}
movies_info = {
    'harry_potter': movie
}


# TODO: Add database support.


def get_movies_infos():
    return list(movies_info.values())


def get_movies_names():
    return [movie.title for movie in get_movies_infos()]


def get_movies():
    return zip(get_movies_infos(), get_movies_names())


def get_movie_by_title(title):
    return movies_info[title]


def confirm_identity(username):
    # if get_jwt_identity() != username:
    #     abort(401)
    return


@app.route('/')
def _():
    return redirect(GET_MOVIES)


# Fetches list of movies based on trending which has (> 95%) users ratings
@app.route(TRENDING_NOW, methods=['GET'])
def trending_now(username):
    confirm_identity(username)

    movies = get_movies_infos()
    print(movies)
    trending = []

    for movie in movies:
        # Checking if movie has more than 95% ratings
        if movie.ratings > 95:
            trending.append(movie)
    return make_response(jsonify(trending), 200)


# Fetches list of movies based on username
@app.route(GET_MOVIES, methods=['GET'])
def movies(username):
    confirm_identity(username)
    movies = get_movies_names()
    return make_response(jsonify(movies), 200)


# User can search for movie based on the title
@app.route(SEARCH_MOVIE, methods=['GET'])
def search_movie(username, title):
    confirm_identity(username)

    if title in movies_info:
        movie = get_movie_by_title(title=title)
        return make_response(jsonify(movie), 200)
    else:
        abort(404)


# User can delete movie based on the title
@app.route(DELETE_MOVIE, methods=['GET', 'POST'])
def delete_movie(username, title):
    confirm_identity(username)
    # movie = get_movie_by_title(title=title)

    if title in movies_info:
        del movies_info[title]
    else:
        abort(404)

    return make_response(jsonify({
        "success": 'Movie Deleted Successfully'
    }), 200)


# User can add/remove movies as per their favourites
@app.route(ADD_TO_FAVOURITE, methods=['POST'])
def add_to_favourite(username, title):
    confirm_identity(username)

    data = jsonify(request.form).json

    if title in movies_info:
        movies_info[title].is_favourite = request.json['is_favourite']
    else:
        abort(404)

    print(data)
    if request.json['is_favourite']:
        message = title + ' has been added to your favourite'
    else:
        message = title + ' has been removed from your favourite'

    return make_response(jsonify({
        "success": message
    }), 200)


# Fetches list of favourite movies based on the username
@app.route(FAVOURITE_MOVIES, methods=['GET'])
def favourite_movies(username):
    confirm_identity(username)

    movies = [movie_name for movie_info, movie_name in get_movies() if movie_info.is_favourite]

    return make_response(jsonify(movies), 200)


# User can add new movie into the database
@app.route(ADD_MOVIE, methods=['POST'])
def add_movie(username):
    confirm_identity(username)
    try:
        title = '_'.join(request.json['title'].tolower().split())
        movies_info[title] = Movie(title=request.json['title'],
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
                                   is_favourite=request.json['is_favourite']
                                   )
    except KeyError:
        abort(400)

    return make_response(jsonify({
        "success": 'Movies Added Successfully'
    }), 201)


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
    app.run(debug=True)
