from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from database.db import db
from database.models import User
import datetime

class SignupApi(Resource):
 def post(self):
   body = request.get_json()

   # Validate request
   newUsername = None if "username" not in body else body["username"]
   newPassword = None if "password" not in body else body["password"]
   if not newUsername or not newPassword or not 5 <= len(newUsername) <= 30 or not 6 <= len(newPassword) <= 30:
      return {"error":"Format request as follows: {\"username\": \"between_5_and_30_chars\", \"password\": \"between_6_and_30_chars\"}"}, 422

   if User.query.filter_by(username=newUsername).first():
      return {"error":"This username is already taken"}

   newUser = User(username = newUsername, password = newPassword)
   newUser.hashPassword()
   
   db.session.add(newUser)
   db.session.commit()
   return {'user id': str(newUser.id)}, 200

class LoginApi(Resource):
   def post(self):
      body = request.get_json()

      # Validate request
      reqUsername = None if "username" not in body else body["username"]
      reqPassword = None if "password" not in body else body["password"]
      if not reqUsername or not reqPassword:
         return {"error":"Format request as follows: {\"username\": \"between_5_and_30_chars\", \"password\": \"between_6_and_30_chars\"}"}, 422

      user = User.query.filter_by(username=reqUsername).first()
      if not user:
         return {'error': 'Username does not exist. Sign up first at /auth/signup'}, 422

      isLoginValid = user.evalPassword(reqPassword)
      if not isLoginValid:
         return {'error': 'Incorrect password'}, 401

      expires = datetime.timedelta(days=30)
      accessToken = create_access_token(identity=str(user.id), expires_delta=expires)
      return {'token': accessToken}, 200

