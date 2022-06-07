from flask_jwt_extended import JWTManager
from flask import Flask

# Flask Initialization
app = Flask(__name__)

# Initialize jwt manager using the secret key
app.config['JWT_SECRET_KEY'] = 'python-flask-microservices'
jwt = JWTManager(app)

