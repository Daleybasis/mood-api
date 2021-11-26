from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from database.models import Mood, User
import datetime

class MoodApi(Resource):
    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())
        moods = []
        previousDate = datetime.datetime(1, 1, 1)
        streak = 1
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
        body = request.get_json()
        user = User.query.get(get_jwt_identity())
        newMood = None
        if "date" in body:
            try:
                newDate = datetime.datetime.strptime(body["date"], '%Y-%m-%d').date()
                newMood = Mood(mood = body["mood"], date = newDate, author=user)
            except ValueError:
                return {'error': 'Incorrect date format. Should be YYYY-MM-DD'}, 422
        else:
            # Will default to current date
            newMood = Mood(mood = body["mood"], author=user)

        db.session.add(newMood)
        db.session.commit()

        return 'Success', 200