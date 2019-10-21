from flask import Blueprint, render_template;

hello_bp = Blueprint("hello_bp", __name__,
	template_folder='templates', static_folder='static');

@hello_bp.route('/', methods=['GET'])
def hello() -> str:
	# need to have a list of degrees

	# TODO get database set up and query db for possible degrees

	# TODO render autocomplete in js like: https://dev.to/sage911/how-to-write-a-search-component-with-suggestions-in-react-d20
    return render_template('hello.html', text='hello world');
