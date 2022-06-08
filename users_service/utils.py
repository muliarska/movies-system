import re
import variables as var


def login_validation(username, postgres_client):
    user = postgres_client.select_user_by_username(username, var.TABLE_NAME)
    if user:
        return user[0][6]
    return False


# Utility method to validate the password
def password_validation(password):
    pwd_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pwd_pattern = re.compile(pwd_regex)
    password_regex_match = re.search(pwd_pattern, password)
    return password_regex_match


# Utility method to validate the email address
def email_validation(email):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email_pattern = re.compile(email_regex)
    email_regex_match = re.search(email_pattern, email)
    return email_regex_match