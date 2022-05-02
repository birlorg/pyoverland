#!/usr/bin/env python3
"""
Authentication library for pyoverlander

Constraints: stick to python standard library for dependencies

Goal: be reasonably secure

Tokens are not stored encrypted, this is arguable bad.

1st, tokens are only used for authorizing the submit form.
if a token leaks, the worst they could do is create some dummy location data for you,
assuming of course there are no big security bugs, obviously.
"""
import json
import logging
import hashlib
import secrets

import sys
import timeit

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class AuthorizationError(Exception):
    """Exception for Auth"""

def authenticate_user(db,email,password):
    """ran by bottle, auth users
    called via main.py/bottle request decorator

    Either raise an exception or return a () of email and extra{}

    uses DB table users w/ columns: email, salt, hashed_password , valid , extra 
    """
    qry = "select email,salt,hashed_password,extra where valid is true and email=?;"
    row = db.execute(qry, (email,)).fetchone()
    if not row:
        log.debug("auth: no valid user entry found for: %s",email)
        raise AuthorizationError({
            "error":True,
            "code":"unauthorized_user",
            "description":"Unauthorized user"
            })
    password = encrypt_password(password,salt=row['salt'])
    if not compare(row['hashed_password'],password):
        log.debug("auth: password compare failed: %s",email)
        raise AuthorizationError({
            "error":True,
            "code":"unauthorized_user",
            "description":"Unauthorized user"
            })
    return row['email'], json.loads(row['extra'])


def authenticate_token(db,token):
    """
    verify authentication token
    called via main.py/bottle request decorator
    uses token table: token int not null primary key, email text, note text

    There is a timing attack here, but we are lazy.
        SQL is doing the comparison, shortening the time if no valid token.
    """
    qry = "select rowid,token,email,device_id,extra from tokens where valid is true and token=?;"
    row = db.execute(qry, (token,)).fetchone()
    if not row:
        log.debug("auth: no valid user entry found for: %s",token)
        raise AuthorizationError({
            "error":True,
            "code":"unauthorized_user",
            "description":"Unauthorized user"
            })
    return {'rowid':row['rowid'], 'email':row['email'], 'device_id':row['device_id'], 'extra':json.loads(row['extra'])}

def encrypt_password(passwd, salt=None, iteration_count=250000):
    """
    encrypt password with salt for iteraton_count times.
    source of values: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63b.pdf
    Grassi Paul A. (June 2017). SP 800-63B-3 – Digital Identity Guidelines, Authentication and Lifecycle Management. NIST. doi:10.6028/NIST.SP.800-63b.

    iteration_count: We default to 250k, In 2017 the recommended min was 10k, we are significantly above that.
    salt: from 800-63B in 2017, 112 was the recommended value. Bumped to 256 bits (32 bytes) for good measure.

    On my crappy VPS @ idle-ish load, it takes 1/3 of a second to encrypt a 64char password.
    To time on your machine just run main().
    You probably don't want to get above 1/3 of a second(.33).
    """
    if not salt:
        salt = secrets.token_bytes(32)
    # convert stuff to bytes if required
    if isinstance(salt, str):
        salt = bytes(salt, "utf-8")
    if isinstance(passwd, str):
        passwd = bytes(passwd, "utf-8")
    hashed = hashlib.pbkdf2_hmac("sha256", passwd, salt, 500000)
    return hashed, salt


def compare(pwd1, pwd2):
    """compare passwords for equality, as securely as possible"""
    return secrets.compare_digest(pwd1, pwd2)


def main(args):
    """main"""
    salt = secrets.token_bytes(32)
    # 50 bytes is roughly a 64 char random password, the sane max amount.
    # more than 64 is arguably more than all the known universe.
    password = secrets.token_bytes(50)

    def enc():
        encrypt_password(password, salt)

    print("encryption of 1 password takes %s seconds " % timeit.timeit(enc, number=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
