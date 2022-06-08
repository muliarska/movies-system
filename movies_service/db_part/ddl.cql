CREATE KEYSPACE movies WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE movies;


CREATE TABLE movies (
    id TEXT,
    username TEXT,
    title TEXT,
    movie_type TEXT,
    ratings INT,
    duration INT,
    age_restriction INT,
    description TEXT,
    cast TEXT,
    genres TEXT,
    category TEXT,
    production TEXT,
    country TEXT,
    is_favourite BOOLEAN,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY ((id), username, title)
);


CREATE TABLE trending_movies (
    id TEXT,
    username TEXT,
    title TEXT,
    ratings INT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY ((id), username, ratings)
);


CREATE TABLE favourite_movies (
    id TEXT,
    username TEXT,
    title TEXT,
    is_favourite BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY ((id), username, title)
);