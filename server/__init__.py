from flask import Flask

from . import hello
from . import db

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():

    	db.init_app(app)

    	app.register_blueprint(hello.hello_bp)

    return app
