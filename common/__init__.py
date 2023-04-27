from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.exceptions import HTTPException


class AppException(HTTPException):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(description=message)
        self.message = message
        self.payload = payload
        if status_code is not None:
            self.code = status_code

    def get_response(self, environ=None):
        response = jsonify({"error": {"message": self.message}})
        response.status_code = self.code
        return response


mongo = PyMongo()
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_SETTINGS')
    mongo.init_app(app)
    cors.init_app(app)

    @app.errorhandler(AppException)
    def handle_exception(e):
        return e.get_response()

    return app
