#!/usr/bin/env python3
""" capture submissions of locations from overland

Docs/urls
 * bottle docs: https://bottlepy.org/docs/0.12/
 * Overland iOS App: https://github.com/aaronpk/Overland-iOS#api
 * Sqlite:  
    * json docs: https://sqlite.org/json1.html

"""
import os
import pprint
import json
import logging
import sqlite3
import sys

import bottle
from bottle import Bottle, auth_basic, run, request, response
import bottle_sqlite as sqlite

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

if not os.isatty(sys.stdin.fileno()):
    TOKEN = sys.stdin.readline()
else:
    log.warning("No TOKEN defined, no authentication done")
    log.warning('to define a token, send it as stdin, i.e.: echo "mytoken" | python main.py')

class JSONErrorBottle(Bottle):
    def default_error_handler(self, err):
        bottle.response.content_type = 'application/json'
        if isinstance(err,Exception):
            if isinstance(err,AuthorizationError):
                #log.info("error exception: %s" % (dir(err))) 
                e = err.body.args[0]
                #log.debug("error exception: %s", type(e))
                log.info("error exception: %s", pprint.pformat(err.body.args))
                return json.dumps({'error':e,'status_code':err.status_code})
        log.info("error handler: %s", pprint.pformat(err))
        #response.content_type = 'application/json'
        return json.dumps(dict(error = err.body, status_code = err.status_code))

app = JSONErrorBottle()

def handle_new_submission(db, data):
    """bottles /submit endpoint calls here to handle processing the data
    return JSON to be sent to end user

    table: 
    locations (json json, timestamp datetime, device_id text, x int, y int, coordinates point, properties text, type text)
    
    Convert to python datetime: datetime.strptime("2010-06-04T21:08:12", "%Y-%m-%dT%H:%M:%S%z")
    """
    log.debug("new submission: %s",pprint.pformat(data))
    for location in data['locations']:
        db.execute('insert into locations VALUES (?,?,?,?,?,?,?,?)',(json.dumps(location),
            location['properties']['timestamp'],
            location['properties']['device_id'],
            json.dumps(location['geometry']['coordinates'][0]),
            json.dumps(location['geometry']['coordinates'][1]),
            json.dumps(location['geometry']['coordinates']),
            json.dumps(location['properties']),
            location['type']
            )
        )
    log.info("saved %d records",len(data['locations']))
    return {'result':'ok'}



class AuthorizationError(Exception):
    """Exception for Auth
    """
    pass

def auth(token):
    """
    verify authentication token
    Should be done better, obviously.
    """
    if not TOKEN:
        log.warning("No TOKEN defined, no authentication done")
        log.warning('to define a token, send it as stdin, i.e.: echo "mytoken" | python main.py')
        return True
    if token == TOKEN:
        return True
    else:
        raise AuthorizationError({'code':'unauthorized','description':'Unauthorized Token'})

def token_from_header():
    auth = bottle.request.headers.get('Authorization', None)
    if not auth:
        raise AuthorizationError({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'})
    elif len(parts) == 1:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Token not found'})
    elif len(parts) > 2:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'})

    return parts[1]

def requires_auth(f):
    """function decorator that requires a bearer token authentication

    update auth() function to auth.
    """
    def decorated(*args, **kwargs):
        try:
            token = token_from_header()
        except AuthorizationError as reason:
            bottle.abort(400, reason)
        try:
            auth(token)
        except AuthorizationError as reason:
            bottle.abort(401, reason)
        return f(*args, **kwargs)
    return decorated


@app.route('/overland/status')
def status():
    """
    """
    #log.debug(pprint.pformat(bottle.request.environ.keys()))
    d = {
            'status':'OK',
            }
    return json.dumps(d)

@requires_auth
@app.post('/overland/submit')
def submit(db):
    """Submit new location request.
    """
    if bottle.request.environ['REMOTE_ADDR'] != '127.0.0.1':
        return json.dumps({'error':'Sorry, unable to accept requests from you'})
    response.content_type = 'application/json'
    log.debug("%s" % request.headers)
    if not request.json:
        log.error("no JSON data received:")
        return json.dumps({'error':"must send json data as content-type: application/json"})
    req = request.json
    log.info("new connection: %s" % (pprint.pprint(req)))
    return json.dumps(handle_new_submission(db,req))
    return json.dumps({'error':'sorry'})

def main(args):
    """main
    start the BG threads and then start serving HTTP traffic.
    """
    db = args[1]
    log.info("Using database: %s",db)
    plugin = sqlite.Plugin(dbfile=db)
    app.install(plugin)
    run(app, host='localhost', port=8080, debug=True)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
