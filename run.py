'''
Main Flask application starting point
'''
from server import create_app
import argparse

app = create_app()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', default=5000, type=int, help='port to run on')
    args = parser.parse_args()
    print(f'running app on port {args.p}')
    app.run(port=args.p, debug=True)
