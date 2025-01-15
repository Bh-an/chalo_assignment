from flask import Flask
from api.app.routes import register_routes

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_routes(app)
    return app