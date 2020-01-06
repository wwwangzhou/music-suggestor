from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # create an instance of Flask class

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://didpckdbmabrtt:bdbcf31a04e52bd0ceba2f2f3c7d1ad43e863ae75a762f54a6fcce5b410519ad@ec2-107-21-214-26.compute-1.amazonaws.com:5432/d68568ks5tqecj'

db = SQLAlchemy(app) # For app initialization


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from arteeas import routes
