from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.routes import initializeRoutes
from database.db import initializeDB

app = Flask(__name__)
app.config.from_pyfile('./.env')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///moods.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

initializeDB(app)
initializeRoutes(api)

app.run()