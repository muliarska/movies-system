from datetime import datetime

class CassandraClient:
    def __init__(self, host, port, keyspace):
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        from cassandra.cluster import Cluster
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)

    def execute(self, query):
        return self.session.execute(query)

    def get_trending_movies(self, username,  table_name):
        query = f"SELECT title FROM {table_name} WHERE username = '{username}' AND ratings > 95 ALLOW FILTERING;"
        data = self.execute(query)
        return data

    def get_movies_data(self, username, table_name):
        query = f"SELECT * FROM {table_name} WHERE username = '{username}' ALLOW FILTERING;"
        data = self.execute(query)
        return data

    def get_by_title(self, username, title, table_name):
        query = f"SELECT * FROM {table_name} WHERE username = '{username}' AND title = '{title}' ALLOW FILTERING;"
        data = self.execute(query)
        return data

    def delete_movie(self, ids, table_names):
        for i in range(len(table_names)):
            query = f"DELETE FROM {table_names[i]} WHERE id = '{ids[i]}';"
            self.execute(query)

    def update_favourite_movies(self, username, title,  table_name):
        current_time = datetime.now()
        query = f"UPDATE {table_name} SET is_favourite = {True}, updated_at = '{current_time}' WHERE username = '{username}' AND title = '{title}';"
        self.execute(query)

    def get_favourite_movies(self, username, table_name):
        query = f"SELECT * FROM {table_name} WHERE username = '{username}' ALLOW FILTERING;"
        data = self.execute(query)
        return data

    def insert_movies_data(self, data_to_insert, table_name):
        query = f"INSERT INTO {table_name} (id, username, title, movie_type, ratings, duration, age_restriction, " \
                f"description, cast, genres, category, production, country, created_at, updated_at)" \
                f"VALUES ('{data_to_insert[0]}', '{data_to_insert[1]}', '{data_to_insert[2]}', '{data_to_insert[3]}'," \
                f"{data_to_insert[4]}, {data_to_insert[5]}, {data_to_insert[6]}, '{data_to_insert[7]}', " \
                f"'{data_to_insert[8]}', '{data_to_insert[9]}', '{data_to_insert[10]}', '{data_to_insert[11]}'," \
                f"'{data_to_insert[12]}','{data_to_insert[13]}', '{data_to_insert[14]}');"
        self.execute(query)

    def insert_favourite_movies_data(self, data_to_insert, table_name):
        query = f"INSERT INTO {table_name} (id, username, title, is_favourite, created_at, updated_at) VALUES " \
                f"('{data_to_insert[0]}', '{data_to_insert[1]}', '{data_to_insert[2]}', {data_to_insert[3]}, '{data_to_insert[4]}', '{data_to_insert[5]}');"
        self.execute(query)

    def insert_movies_ratings_data(self, data_to_insert, table_name):
        query = f"INSERT INTO {table_name} (id, username, title, ratings, created_at, updated_at) VALUES " \
                f"('{data_to_insert[0]}', '{data_to_insert[1]}', '{data_to_insert[2]}', {data_to_insert[3]}, '{data_to_insert[4]}', '{data_to_insert[5]}');"
        self.execute(query)

    def close(self):
        self.session.shutdown()