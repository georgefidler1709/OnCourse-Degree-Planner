from flask import Flask;

from . import hello;

def create_app() -> Flask:
    app = Flask(__name__);
    app.config.from_mapping(SECRET_KEY='test');

    app.register_blueprint(hello.bp);

    return app;
