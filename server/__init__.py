from flask import Flask;

from . import degrees;
from . import db;

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():

    	db.init_app(app)

    	app.register_blueprint(degrees.degrees_bp)

    return app
