from flask import Flask
from flask_restx import Resource, Api
from flask_cors import CORS
from datetime import datetime, timezone
import data.roles as rls
import sys
import os
import subprocess
from collections import deque

# Import the endpoints from separate modules
from server.text_endpoints import api as text_api
from server.people_endpoints import api as people_api
from server.manu_endpoints import api as manu_api

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)
CORS(app)
api = Api(app)

# Register the namespaces from other modules
api.add_namespace(text_api, path='')
api.add_namespace(people_api, path='')
api.add_namespace(manu_api, path='')

DATE = datetime.now(timezone.utc).isoformat()  # should get the actual date
DATE_RESP = 'Date'
EDITOR = 'ayy9673@nyu.edu'
EDITOR_RESP = 'Editor'
ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
MESSAGE = 'Message'
PUBLISHER = 'FirstClass'
PUBLISHER_RESP = 'Publisher'
RETURN = 'Return'
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TITLE = 'The Journal'
ROLES_EP = '/roles'


# figure out how to structure endpoints to clump classes together

@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(ROLES_EP)
class Roles(Resource):
    """
    This class handles reading person roles.
    """
    def get(self):
        """
        Retrieve the journal person roles.
        """
        return rls.read()


@api.route(TITLE_EP)
class JournalTitle(Resource):
    def get(self):
        """
        Retrieve jounal info including title, editor, and publisher
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            PUBLISHER_RESP: PUBLISHER
        }


@api.route('/dev/info')
class DevInfo(Resource):
    """
    Developer endpoint to show environment and runtime debug info.
    Should NOT be exposed in production.
    """
    def get(self):
        return {
            "server_time": datetime.utcnow().isoformat() + "Z",
            "python_version": sys.version,
            "cwd": os.getcwd(),
            "env": dict(os.environ) if app.debug else "Hidden in production",
            "routes": sorted(
                rule.rule for rule in api.app.url_map.iter_rules()
            )

        }


# Helper function to decode the subprocess output
def format_output(result):
    return result.stdout.decode('utf-8').strip()


@api.route('/logtail')
class LogTail(Resource):
    """
    This endpoint returns the tail of the specified log.
    """
    def get(self):
        ELOG_LOC = '/var/log/system.log'

        # Execute the tail command on ELOG_LOC
        result = subprocess.run(
            f'tail {ELOG_LOC}',
            shell=True,
            stdout=subprocess.PIPE
        )

        return {"log": format_output(result)}


@api.route('/security/logs')
class SecurityLogs(Resource):
    """
    Return the last N lines of the security.log file.
    """
    def get(self):
        # replace with your path, if different
        log_path = 'security.log'
        log_path = 'security.log'
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                # pull in only the last 100 lines
                lines = deque(f, maxlen=100)
                lines = deque(f, maxlen=100)
        except FileNotFoundError:
            lines = []

        # strip trailing newlines
        return {
            'logs': [line.rstrip('\n') for line in lines]
        }
