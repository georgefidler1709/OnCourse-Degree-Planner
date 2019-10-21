from flask import Blueprint, render_template;

hello_bp = Blueprint("hello_bp", __name__,
	template_folder='templates', static_folder='static');

@hello_bp.route('/', methods=['GET'])
def hello() -> str:
    return render_template('hello.html', text='hello world');
