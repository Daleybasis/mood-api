# mood-api
A simple proof-of-concept API that lets users log in and post their mood on any given date.  Their posted moods can then be retrieved, along with a streak counter for how many days in a row the user has submitted a mood.  This API was developed on Linux (WSL) using Python 3.8 and Flask.

## Installation
After cloning the repo, `cd` into the mood-api directory.  If you haven't installed pipenv already, enter:

`pip install --user pipenv`

to do so.  Next, install the project's dependencies in a virtual environment: 

`pipenv install`


## Running the Development Server
While in the mood-api directory, enter the virtual environment:

`pipenv shell`

Finally, from within the shell, start the development server at `http://localhost:5000` with the following command:

`python3 app.py`

## Interacting with the API
The API receives JSON requests and returns JSON responses.  I used Postman for easy testing during development.

### /auth
Register accounts at `/auth/signup`.

Log into existing accounts at `/auth/login`.  The API responds to the login `POST` request with an authentication token that should be used with `/mood`.

`POST` request bodies sent to either URL should use the following format:

`{"username": "between_5_and_30_chars", "password": "between_6_and_30_chars"}`

### /mood
Both `GET` and `POST` requests need a `bearer` authentication header with the token returned from `POST`ing to `/auth/login`.

`POST` request bodies should use the following format:

`{"mood": "happy", "date": "2021-11-29"}`

The `"date"` attribute can be omitted.  If it is, the current date is stored.
