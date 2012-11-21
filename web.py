import data_access

import rauth

secret = open('../reddit_secret.txt').read()

def app(environ, start_response):
  data = "Hello, World!\n"
  start_response("200 OK", [
      ("Content-Type", "text/plain"),
      ("Content-Length", str(len(data)))
  ])
  return iter([data])

