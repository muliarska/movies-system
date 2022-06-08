# User API endpoint
API_PATH = '/movies_api'
LOG_IN = API_PATH + '/log_in'
LOG_OUT = API_PATH + '/log_out'
CHECK_LOG_IN = API_PATH + '/check_log_in'
SIGN_UP = API_PATH + '/sign_up'
USER_PROFILE = API_PATH + '/profile/<username>'
UPDATE_PROFILE = API_PATH + '/update_profile/<username>'
CHANGE_PASSWORD = API_PATH + '/change_password/<username>'
DELETE_ACCOUNT = API_PATH + '/delete_account/<username>'



# error msg

error_pwd_validation_msg = 'Password must contain at least 6 characters, ' + \
                           'including Upper/Lowercase, special characters and numbers'


# postgres configs

DB_NAME = "users_db"
USER = "test_user"
HOST = "postgres-db"
PASSWORD = "1234"
PORT = "5432"
TABLE_NAME = "users"
