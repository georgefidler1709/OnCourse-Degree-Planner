from flask import Flask

from . import hello
from . import db_setup

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():

    	db_setup.init_app(app)

    	app.register_blueprint(hello.hello_bp)

    return app
