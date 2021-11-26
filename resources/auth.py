from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from database.db import db
from database.models import User
import datetime

class SignupApi(Resource):
 def post(self):
    body = request.get_json()
    newUser = User(username = body["username"], password = body["password"])
    newUser.hashPassword()
    
    db.session.add(newUser)
    db.session.commit()

    id = newUser.id
    return {'user id': str(id)}, 200

class LoginApi(Resource):
   def post(self):
      body = request.get_json()
      user = User.query.filter_by(username=body["username"]).first()

      isLoginValid = user.evalPassword(body['password'])
      if not isLoginValid:
         return {'error': 'Username or password invalid'}, 401

      expires = datetime.timedelta(days=30)
      accessToken = create_access_token(identity=str(user.id), expires_delta=expires)
      return {'token': accessToken}, 200