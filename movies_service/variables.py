# Movies API endpoint

API_PATH = '/movies_api'
TRENDING_NOW = API_PATH + '/trending_now/<username>'
GET_MOVIES = API_PATH + '/movies/<username>'
ADD_MOVIE = API_PATH + '/add_movie/<username>'
SEARCH_MOVIE = API_PATH + '/search_movie/<title>/<username>'
DELETE_MOVIE = API_PATH + '/delete_movie/<title>/<username>'
ADD_TO_FAVOURITE = API_PATH + '/add_to_favourites/<title>/<username>'
FAVOURITE_MOVIES = API_PATH + '/favourite_movies/<username>'


# Cassandra configs
HOST = 'cassandra-node'
PORT = 9042
KEYSPACE = 'movies'
MOVIES_TABLE_NAME = "movies"
FAVOURITES_TABLE_NAME = "favourite_movies"
TRENDING_TABLE_NAME = "trending_movies"


# додати айдішки треба