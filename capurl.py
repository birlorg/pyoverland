"""Capability URL's
https://www.w3.org/TR/capability-urls/

permissions are just a python set() of strings.
"""

import uuid

known_capabilities = (
	'admin', # administrator, can do everything
	'now', # can see now page
	'history', # can see history page
	'submit', # can submit new entries(Overlander app)
	'delegate', # can delegate this set of caps to someone else
    )

def gen_capability(perms: set):
    """
    generate a capability
    """
    id = str(uuid.uuid4())

def auth_check_oneof(needed: set,perms: set) -> bool:
    """
    given a set(needed), ensure set(perms) has at least 1 of them
    """
    assert isinstance(needed,set())
    assert isinstance(perms,set())
    # we need one of needed
    if len(needed - roles) < len(needed):
        return True
    return False

def auth_check_one(needed: str, perms: set) -> bool:
    """
    given a str ensure it's in the set
    """
    assert isinstance(perms,set())
    if needed in perms:
        return True
    return False

def save(db,cap,perms,meta):
    """save to DB
    """
    perms = json.dumps(list(perms))
    
    db.execute("insert into capabilities () VALUES ();")

def load(db,cap):
    """load from DB

 capabilities {
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
	"""
	d = db.execute("select * from capabilities where cap=?", cap).fetchone()
    d['perms'] = set(json.loads(d['perms']))
	d['extra'] = json.loads(d['extra'])
	return d
