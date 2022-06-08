from psycopg2 import connect
from datetime import datetime

class PostgresClient:
    def __init__(self, host, port, db_name, password, user):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.password = password
        self.user = user
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = connect(
            dbname=self.db_name,
            user=self.user,
            host=self.host,
            password=self.password,
            port=self.port
        )
        self.cursor = self.conn.cursor()

    def insert_records(self, data_to_insert, table_name):
        query = f"INSERT INTO {table_name} (user_id, username, password, name, email, dob, log_in) " \
                f"VALUES ('{data_to_insert[0]}', '{data_to_insert[1]}', '{data_to_insert[2]}'," \
                f" '{data_to_insert[3]}', '{data_to_insert[4]}', '{data_to_insert[5]}', {data_to_insert[6]});"
        self.cursor.execute(query)

    def update_record(self,  user_id, field_to_update, data_to_change, table_name):
        current_time = datetime.now()
        query = f"UPDATE {table_name} SET {field_to_update} = '{data_to_change}', updated_at = '{current_time}' WHERE user_id = '{user_id}';"
        self.cursor.execute(query)

    def delete_record(self, user_id,  table_name):
        query = f"DELETE FROM {table_name} WHERE user_id = '{user_id}';"
        self.cursor.execute(query)

    def select_user_by_username(self, username, table_name):
        query = f"SELECT * from {table_name} WHERE username = '{username}';"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

    def close_cursor(self):
        self.cursor.close()

    def close_conn(self):
        self.conn.close()


# 0         1         2         3     4      5    6
#[user_id, username, password, name, email, dob, sign_in]