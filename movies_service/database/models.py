from flask_mongoengine import MongoEngine

db = MongoEngine()


class Thumbnails(db.Document):
    type = db.StringField(required=True)
    client = db.StringField(required=True)
    size = db.StringField(required=True)
    path = db.StringField(required=True)


class Media(db.Document):
    type = db.StringField(required=True)
    client = db.StringField(required=True)
    path = db.StringField(required=True)


class Subtitles(db.Document):
    language = db.StringField(required=True)
    path = db.StringField(required=True)


class Movies(db.Document):
    title = db.StringField(required=True)
    movie_type = db.StringField(required=True)
    ratings = db.IntField(required=True)
    duration = db.IntField(required=True)
    age_restriction = db.StringField(required=True)
    timestamp = db.IntField(required=True)
    thumbnails = db.ListField(db.ReferenceField(Thumbnails))
    media = db.ListField(db.ReferenceField(Media))
    subtitles = db.ListField(db.ReferenceField(Subtitles))
    description = db.StringField(required=True)
    cast = db.ListField(db.StringField(required=True))
    genres = db.ListField(db.StringField(required=True))
    category = db.StringField(required=True)
    production = db.StringField(required=True)
    country = db.StringField(required=True)
    is_favourite = db.BooleanField(required=True)


def get_movies():
    return Movies.objects()


def get_movie_by_title(title=''):
    # return Movies.objects.get(title=title)
    return Movies.objects(title=title).first()


def get_favourite_movies():
    return Movies.objects(is_favourite=True)






