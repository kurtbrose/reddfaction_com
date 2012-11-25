import os
import base64
import rauth
import rauth.service
from werkzeug.wrappers import Response
from werkzeug.utils import redirect
import requests
import json

import clastic

import data_access
from data_access import User

def hello_world():
    return Response("Hello, World!")

def login(reddit_auth):
    authorize_url = reddit_auth.get_authorize_url(
        response_type="code",
        scope="identity",
        state=base64.b64encode(os.urandom(32)), #reddit doesn't like unprintable states
        redirect_uri = "http://reddfaction.com/auth")
    return redirect(authorize_url)

def auth(request, reddit_auth, db_session):
    code = request.args["code"]
    resp = reddit_auth.get_access_token(
        auth=(reddit_auth.consumer_key, reddit_auth.consumer_secret),
        data = { 
            "grant_type" : "authorization_code", 
            "code" : code, 
            "redirect_uri" : "http://reddfaction.com/auth",
        }
    )
    if 'access_token' not in resp.content:
        return redirect("/login") #assuming this means token has expired
    access_token = resp.content['access_token']
    resp = requests.get("https://oauth.reddit.com/api/v1/me.json", 
        headers={"Authorization":"bearer "+access_token})
    if resp.status_code != 200:
        raise Exception("response "+str(resp.status_code)+" "+resp.reason)
    reddit_username = json.loads(resp.content)['name']
    if not db_session.query(User).filter(User.reddit_name==reddit_username).count():
        db_session.add(User(reddit_username))
        print "new user"
    return Response("Hello, "+str(reddit_username))

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

    app = clastic.Application(routes, resources, middlewares=[data_access.DBSessionMiddleware()])
    return app

app = create_app()

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, app, use_debugger=True, use_reloader=True)
