from .mood import MoodApi
from .auth import SignupApi, LoginApi

def initializeRoutes(api):
    api.add_resource(MoodApi, '/mood')
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')