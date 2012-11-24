import os
import rauth
import rauth.service
from werkzeug.wrappers import Response
from werkzeug.utils import redirect

import clastic

import data_access

def hello_world():
    return Response("Hello, World!")

def login(reddit_auth):
    authorize_url = reddit_auth.get_authorize_url(
        response_type="code",
        scope="identity",
        state=os.urandom(20),
        redirect_uri = "http://reddfaction.com/auth")
    return redirect(authorize_url)

def auth(request, reddit_auth):
    code = request.args["code"]
    access_token = reddit_auth.get_access_token(
        auth=(reddit_auth.consumer_key, reddit_auth.consumer_secret),
        data = { 
            "grant_type" : "authorization_code", 
            "code" : code, 
            "redirect_uri" : "http://reddfaction.com/auth",
        }
    ).content['access_token']
    reddit_username = reddit_auth.get(
        "https://oauth.reddit.com/api/v1/me", access_token=access_token).content
    return Response("Hello, "+reddit_username)

def create_app():
    #set up resources
    reddit_secret = open('../reddit_secret.txt').read()
    reddit_auth = rauth.service.OAuth2Service(
        name="reddit",
        consumer_key="oUuXcyc6EfstQw",
        consumer_secret = reddit_secret,
        access_token_url="https://ssl.reddit.com/api/v1/access_token",
        authorize_url="https://ssl.reddit.com/api/v1/authorize")
    resources = {"reddit_auth":reddit_auth}
    #set up routes
    passthru = lambda a: a
    #TODO: templates/rendering
    routes = [
        ('/',      hello_world, passthru),
        ('/login', login,       passthru),
        ('/auth',  auth,        passthru),
    ]

    app = clastic.Application(routes, resources)
    return app

app = create_app()

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, app, use_debugger=True, use_reloader=True)
