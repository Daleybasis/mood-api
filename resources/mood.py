from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from database.models import MoodSubmission, User
import datetime

class MoodApi(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        moods = []
        previousDate = datetime.datetime(1, 1, 1)
        streak = 0
        for mood in user.moods:
            moods.append({"user": mood.userID, "date": mood.date.strftime('%Y-%m-%d'), "mood": mood.mood})

            if previousDate + datetime.timedelta(days=1) == mood.date:
                streak += 1
            else:
                streak = 1

            previousDate = mood.date

        return {"streak": streak, "moods": moods}, 200

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            user = User.query.get(get_jwt_identity())

            newSubmission = None
            if "date" in body:
                newDate = datetime.datetime.strptime(body["date"], '%Y-%m-%d').date()
                newSubmission = MoodSubmission(mood = body["mood"], date = newDate, author=user)

            else:
                # Will default to current date
                newSubmission = MoodSubmission(mood = body["mood"], author=user)

            db.session.add(newSubmission)
            db.session.commit()

            return 'Success', 200
        except ValueError:
            return {'error': 'Incorrect date format. Should be YYYY-MM-DD'}, 422
        except KeyError:
            return {"error":"Request must have a \"mood\" attribute"}, 422
