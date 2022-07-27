#!/usr/bin/env python3
""" capture submissions of locations from overland

Docs/urls
 * bottle docs: https://bottlepy.org/docs/0.12/
 * Overland iOS App: https://github.com/aaronpk/Overland-iOS#api
 * Sqlite:
    * json docs: https://sqlite.org/json1.html

"""
from datetime import datetime, date, timedelta, timezone
import os
import pprint
import json
import logging
import sqlite3
import sys
import time

import bottle
from bottle import Bottle, run, request, response, static_file, template, auth_basic
bottle.BaseRequest.MEMFILE_MAX = 202400
import bottle_sqlite as sqlite
import authlib
import weatherapi

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

tz_mst = timezone(timedelta(hours=-7), "MST")

# read from stdin only if there is something there to read
# if not os.isatty(sys.stdin.fileno()):
#    TOKEN = sys.stdin.readline()

global myconfig

def fix_environ_middleware(app):
    def fixed_app(environ, start_response):
        global myconfig
        if len(myconfig.keys()) > 0:
            #log.debug('url:%s',myconfig['url_scheme'])
            if 'url_scheme' in myconfig:
                environ['wsgi.url_scheme'] = myconfig['url_scheme']
            if 'url_domain' in myconfig:
                environ['HTTP_X_FORWARDED_HOST'] = myconfig['url_domain']
            if 'url_proxy_hack' in myconfig:
                ph = myconfig['url_proxy_hack'] 
                phlen = len(ph)
                if ph == environ['PATH_INFO'][:phlen]:
                    environ['PATH_INFO'] = environ['PATH_INFO'].replace(ph,'',1)
            #log.debug('hacks applied, new path:%s',environ['PATH_INFO'])
        return app(environ, start_response)
    return fixed_app


class JSONErrorBottle(Bottle):
    """Hack Bottle to respond in JSON for errors instead of HTML."""

    def default_error_handler(self, res):
        bottle.response.content_type = "application/json"
        if isinstance(res.body, AuthorizationError):
            err = res.body.args[0]
            # log.debug("error exception: %s", type(e))
            log.info("error exception: %s", pprint.pformat(res.body.args))
            return json.dumps({"error": err, "status_code": res.status_code})
        if isinstance(res, AuthorizationError):
            err = res.body.args[0]
            # log.debug("error exception: %s", type(e))
            log.info("error exception: %s", pprint.pformat(res.body.args))
            return json.dumps({"error": err, "status_code": res.status_code})
        else:
            log.info("error handler: %s", pprint.pformat(res))
            # response.content_type = 'application/json'
            r = json.dumps(dict(error=res.body, status_code=res.status_code))
            print(r)
            return r


app = JSONErrorBottle()
app.wsgi = fix_environ_middleware(app.wsgi)

def handle_new_submission(db, data, token):
    """bottles /submit endpoint calls here to handle processing the data
    return JSON to be sent to end user

    create table is in README.md

    """
    token_id = token["rowid"]
    device_id = token["device_id"]
    # log.debug("new submission: %s", pprint.pformat(data.keys()))
    for location in data["locations"]:
        if location["properties"]["device_id"] != device_id:
            log.warning(
                "device ID's do not match between token(%s) and data(%s)",
                device_id,
                location["properties"]["device_id"],
            )
        db.execute(
            "insert into locations VALUES (?,?,?,?,?,?,?,?)",
            (
                json.dumps(location),
                location["properties"]["timestamp"],
                location["properties"]["device_id"],
                json.dumps(location["geometry"]["coordinates"][1]),
                json.dumps(location["geometry"]["coordinates"][0]),
                json.dumps(location["properties"]),
                location["type"],
                token_id,
            ),
        )
    log.info("saved %d records", len(data["locations"]))
    return {"result": "ok"}


class AuthorizationError(Exception):
    """Exception for Auth"""


def requires_auth(func, db):
    """function decorator that requires authentication
    we accept http basic auth.
    this handles the bottle side of auth.
    the rest of auth is in authlib.py, calling:
        authlib.authenticate_user()
    """

    def decorated(*args, **kwargs):
        if bottle.request.environ["REMOTE_ADDR"] != "127.0.0.1":
            return json.dumps({"error": "Sorry, unable to accept requests from you"})
        user, password = request.auth or (None, None)
        if user is None or not authlib.authenticate_user(db, user, password):
            err = bottle.HTTPError(401, text)
            err.add_header("WWW-Authenticate", 'Basic realm="%s"' % realm)
            return err
        return func(*args, **kwargs)

    return decorated


@app.route("/status")
def status():
    """return a status for monitor checking."""
    #log.debug(pprint.pformat(bottle.request.environ.keys()))
    ret = {
        "status": "OK",
    }
    return json.dumps(ret)


@app.post("/submit/<token>")
def submit(db, token):
    """Submit new location request."""
    response.content_type = "application/json"
    try:
        token = authlib.authenticate_token(db, token)
    except AuthorizationError as reason:
        bottle.abort(401, reason)
    if not request.json:
        log.error("no JSON data received:")
        return json.dumps(
            {"error": "must send json data as content-type: application/json"}
        )
    req = request.json
    return json.dumps(handle_new_submission(db, req, token))


@app.route("/static/<filepath:path>")
def server_static(filepath):
    # headers = dict()
    response.set_header("Cache-Control", "public, max-age=120")
    rootpath = "/home/zie/src/pyoverland/static/"
    log.debug("rootpath:%s", rootpath)
    # headers['Cache-Control'] = "public, max-age=600"
    return static_file(filepath, root=rootpath)  # , headers=headers)

# @requires_auth
@app.get("/now")
def now(db):
    """show most recent location"""
    log.info("now: Request from:%s" % bottle.request.environ['HTTP_X_FORWARDED_FOR'])
    qry = "select timestamp,lat,long from locations order by timestamp desc limit 1;"
    row = db.execute(qry).fetchone()
    # Convert to python datetime:
    now_dt = datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
    az_time = now_dt.astimezone(tz_mst)
    lat = row["lat"]
    long = row["long"]
    big_lat = str(lat)[0:7]
    big_long = str(long)[0:8]
    omap_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={long}#map=12%2F{big_lat}%2F{big_long}&layers=N"
    amap_url = f"https://maps.apple.com/?sll={lat},{long}&address=%28{lat}%2C{long}%29&z=10&t=m"
    weather = weatherapi.fetch_weather(big_lat,big_long)
    now = {
        "timestamp": row["timestamp"],
        "human_time": az_time.strftime("%Y/%m/%d %I:%M:%S %p %Z"),
        "big_lat": big_lat,
        "big_long": big_long,
        "latitude": lat,
        "longitude": long,
        "openstreetmap_url": omap_url,
        "apple_maps_url": amap_url,
        "time_ago": time_ago(now_dt.timestamp()),
        "weather": weather,
    }
    return template("now", now=now)

@app.get("/history")
def history(db):
    """Show all history"""
    log.info("history: Request from:%s" % bottle.request.environ['HTTP_X_FORWARDED_FOR'])
    qry = "select timestamp,lat,long from locations where date(timestamp) > DATE('now', '-30 days') order by timestamp desc;" 
    rows = db.execute(qry).fetchall()
    dat = []
    for row in rows:
        # Convert to python datetime:
        now_dt = datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
        az_time = now_dt.astimezone(tz_mst)
        lat = row["lat"]
        long = row["long"]
        big_lat = str(lat)[0:7]
        big_long = str(long)[0:8]
        url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={long}#map=12%2F{big_lat}%2F{big_long}&layers=N"
        now = {
            "timestamp": row["timestamp"],
            "human_time": az_time.strftime("%Y/%m/%d %I:%M:%S %p %Z"),
            "big_lat": big_lat,
            "big_long": big_long,
            "latitude": lat,
            "longitude": long,
            "openstreetmap_url": url,
            "time_ago": time_ago(now_dt.timestamp()),
        }
        dat.append(now)
    step = 0
    if len(dat) > 1000:
        length = len(dat)
        step = int(length/1000)
        log.info("length > 1000 @ %s, stepping by %s" % (length, step))
        dat = dat[0:length:step]
    log.info("sending %s records to user" % len(dat))
    return template("history", dat=dat, step=step)

def time_ago(ts):
    """calculate a human understandable time ago, given a unix timestamp"""
    return " "  # time.time()-ts


def create_db(dbpath):
    """create a new DB

    This is misery, but it works.
    During dev, I altered columns and stuff a lot, so I created this mess to recreate the DB every time
    while only defining the tables and columns once.
    obviously some sort of ORM would be better, but I want no dependencies.

    So we have this:

    CREATE TRIGGER locations_update_audit AFTER UPDATE ON locations
    BEGIN
       INSERT INTO audit_log(table_name, event_type, event_date, table_id, old, new) VALUES ('locations','update',datetime('now'), OLD.rowid, json_object(OLD),json_object(NEW) );
       END;
       CREATE TRIGGER tokens_insert_audit AFTER INSERT on tokens
       BEGIN
       INSERT INTO audit_log(table_name, event_type, event_date, table_id, new) VALUES ('tokens','insert',datetime('now'), NEW.rowid,json_object('token',NEW.token,'email',NEW.email,'valid',NEW.valid,'device_id',NEW.device_id,'extra',NEW.extra,'note',NEW.note) );
       END;
       insert into tokens capabilities ('mytoken','me@example.com','["admin"]','True,'myphone','','token for my iphone');
    """
    tables = {
        "locations": {
            "json": "JSON",
            "timestamp": "DATETIME",
            "device_id": "TEXT",
            "lat": "FLOAT",
            "long": "FLOAT",
            "properties": "TEXT",
            "type": "TEXT",
            "token_id": "INTEGER REFERENCES tokens",
        },
        "audit_log": {
            "table_name": "TEXT",
            "event_type": "TEXT",
            "event_date": "TIMESTAMP",
            "table_id": "INTEGER",
            "old": "JSON",
            "new": "JSON",
            "message": "TEXT",
        },
        "capabilities": {
            "rowid": "INTEGER PRIMARY KEY",
            "token": "TEXT NOT NULL UNIQUE",
            "email": "TEXT NOT NULL UNIQUE",
            "perms": "JSON",
            "used": "INTEGER",
            "valid": "BOOL",
            "device_id": "TEXT",
            "extra": "JSON",
            "note": "TEXT",
        },
        "users": {
            "email": "TEXT not null unique",
            "salt": "TEXT",
            "hashed_password": "TEXT",
            "valid": "BOOL",
            "extra": "JSON",
            "note": "JSON",
        },
        "config": {"key": "TEXT NOT NULL UNIQUE", "VALUE": "TEXT"},
    }
    if os.path.exists(dbpath):
        raise FileExistsError(
            {
                "dbpath": dbpath,
                "description": "This file already exists, will not overwrite.",
            }
        )
    db = sqlite3.connect(dbpath)
    db.row_factory = sqlite3.Row
    for table, columns in tables.items():
        column_text = ""
        audit_insert = ""
        for k, v in columns.items():
            column_text += " %s %s," % (k, v)
            audit_new = " '%s',NEW.%s," % (k, k)
            audit_old = " '%s',OLD.%s," % (k, k)
        # cut last ,
        column_text = column_text[:-1]
        audit_new = audit_new[:-1]
        audit_old = audit_old[:-1]
        table_qry = f"CREATE TABLE {table} ({column_text});"
        print(table_qry)
        db.execute(table_qry)
        audit_log_columns = ",".join(list(tables["audit_log"]))
        trigger_insert_name = f"{table}_insert_audit"
        audit_insert_qry = (
            f"CREATE TRIGGER {trigger_insert_name} AFTER INSERT ON {table}"
            f" BEGIN"
            f" INSERT INTO audit_log({audit_log_columns})"
            f" VALUES ("
            f" '{table}',"
            f" 'insert',"
            f" datetime('now'),"
            f" NEW.rowid,"
            f" 'null',"
            f" json_object({audit_new}),"
            f" 'created by trigger {trigger_insert_name}'"
            f" );"
            f" END;"
        )
        print(audit_insert_qry)
        db.execute(audit_insert_qry)
        for event_type in ("update", "delete"):
            trigger_name = f"{table}_{event_type}_audit"
            audit_qry = (
                f"CREATE TRIGGER {trigger_name} AFTER {event_type.upper()} ON {table}"
                f" BEGIN"
                f" INSERT INTO audit_log({audit_log_columns})"
                f" VALUES ("
                f" '{table}',"
                f" 'update',"
                f" datetime('now'),"
                f" NEW.rowid,"
                f" json_object({audit_old}),"
                f" json_object({audit_new}),"
                f" 'created by trigger {trigger_name}'"
                f" );"
                f" END;"
            )
        print(audit_qry)
        db.execute(audit_qry)
    db.commit()
    db.close()
    print("database created %s" % dbpath)
    return 0

def setup_myconfig(db):
    """
    Allow one to hack the WSGI stuff for reverse proxies.
    if you host on a path say /overland, 
    then url_proxy_hack will fix that up so /now works in routing.

    inserts:

    sqlite> insert into config VALUES ('url_scheme','https');
    sqlite> insert into config VALUES ('url_domain','example.com');
    sqlite> insert into config VALUES ('url_proxy_hack','/overland');
    """
    conf = {}
    c = sqlite3.connect(db)
    qry = "select key,value from config where key in ('url_scheme','url_domain','url_proxy_hack')"
    rows = c.execute(qry).fetchall()
    global myconfig
    myconfig = dict(rows)
    log.debug("setting up hacks: %s ",pprint.pformat(myconfig.keys()))
    #log.debug("setup_myconfig: %s", pprint.pformat(myconfig))

def main(args):
    """main
    start the BG threads and then start serving HTTP traffic.
    """
    db = args[1]
    if db == "newdb":
        sys.exit(create_db(args[2]))
    log.info("Using database: %s", db)
    setup_myconfig(db)
    plugin = sqlite.Plugin(dbfile=db)
    app.install(plugin)
    run(app, host="localhost", port=8080, debug=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
