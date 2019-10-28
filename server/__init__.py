from flask import Flask

from . import hello
from . import db_setup

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
    	db_setup.init_app(app)

    # Populate CORS header (necessary if we are using two webservers)
    def add_cors_headers(response):
        # TODO (kevin): this is not ideal, we should figure out a way to
        # selectively exclude our react webserver
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    app.after_request(add_cors_headers)

    return app
