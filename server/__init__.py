from flask import Flask;

from . import hello;
from . import db;

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
    	app.register_blueprint(hello.hello_bp)

    return app
