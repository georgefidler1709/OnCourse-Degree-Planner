from flask import Flask;

from . import hello;

def create_app() -> Flask:
    app = Flask(__name__);
    app.config.from_object('config.Config');

    with app.app_context():
    	app.register_blueprint(hello.hello_bp);

    print("===> returning app")
    return app;
