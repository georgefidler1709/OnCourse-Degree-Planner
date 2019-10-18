from flask import Blueprint, render_template;

bp = Blueprint("hello", __name__, url_prefix='/hello');

@bp.route('')
def hello() -> str:
    return render_template('hello.html', text='hello world');
