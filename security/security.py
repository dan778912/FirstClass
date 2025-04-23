from functools import wraps
import logging
import json
from logging.handlers import RotatingFileHandler
from functools import wraps

# import data.db_connect as dbc

"""
Our record format to meet our requirements (see security.md) will be:

{
    feature_name1: {
        create: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        read: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        update: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        delete: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
    },
    feature_name2: # etc.
}
"""


# set up a dedicated security logger that writes to security.log
logger = logging.getLogger('security')
logger.setLevel(logging.INFO)

# rotate after 5 MB, keep 2 backups
handler = RotatingFileHandler('security.log',
                              maxBytes=5*1024*1024,
                              backupCount=2,
                              encoding='utf-8')
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(message)s'
))
logger.addHandler(handler)


COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'
LOGIN_KEY = 'login_key'

# Features:
PEOPLE = 'people'
BAD_FEATURE = 'baaaaad feature'

PEOPLE_MISSING_ACTION = READ
GOOD_USER_ID = 'ejc369@nyu.edu'

security_recs = None
# These will come from the DB soon:
temp_recs = {
    PEOPLE: {
        CREATE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                'Bad check': True,
            },
        },
    },
}


def is_valid_key(user_id: str, login_key: str):
    """
    This is just a mock of the real is_valid_key() we'll write later.
    """
    return True


def check_login(user_id: str, **kwargs):
    if LOGIN_KEY not in kwargs:
        return False
    return is_valid_key(user_id, kwargs[LOGIN_KEY])


CHECK_FUNCS = {
    LOGIN: check_login,
    # IP_ADDRESS: check_ip,
}


def read() -> dict:
    global security_recs
    # dbc.read()
    security_recs = temp_recs
    return security_recs


def needs_recs(fn):
    """
    Should be used to decorate any function that directly accesses sec recs.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if not security_recs:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    if feature_name in security_recs:
        return security_recs[feature_name]
    else:
        return None


@needs_recs
def is_permitted(feature_name: str, action: str,
                 user_id: str, **kwargs) -> bool:

    prot = read_feature(feature_name) or {}
    action_cfg = prot.get(action)

    # default-deny if no config exists
    if action_cfg is None:
        allowed = False
    else:
        # user_list check
        ul = action_cfg.get(USER_LIST, [])
        if ul and user_id not in ul:
            allowed = False
        else:
            # run all checks
            allowed = True
            for ck, param in action_cfg.get(CHECKS, {}).items():
                if ck not in CHECK_FUNCS or not CHECK_FUNCS[ck](user_id, **{ck: param, **kwargs}):
                    allowed = False
                    break

    # **LOG IT** before returning
    logger.info(json.dumps({
        'feature': feature_name,
        'action':   action,
        'user':     user_id,
        'allowed':  allowed,
        'params':   kwargs
    }))

    return allowed