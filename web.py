import rauth
from werkzeug.wrappers import Response
import clastic

import data_access

def root():
    return Response("Hello, World!")

def create_app():
    reddit_token = open('../reddit_secret.txt').read()

    app = clastic.Application([('/', root, lambda a: a)], {"reddit_token":reddit_token})
    return app

app = create_app()

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, app, use_debugger=True, use_reloader=True)
