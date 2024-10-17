"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask  # , request
from flask_restx import Resource, Api  # Namespace, fields
from flask_cors import CORS

import werkzeug.exceptions as wz
import data.people as ppl

app = Flask(__name__)
CORS(app)
api = Api(app)

DATE = '2024-09-24'
DATE_RESP = 'Date'
EDITOR = 'ayy9673@nyu.edu'
EDITOR_RESP = 'Editor'
ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
PEOPLE_EP = '/people'
PUBLISHER = 'FirstClass'
PUBLISHER_RESP = 'Publisher'
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TITLE = 'The Journal'


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


@api.route(TITLE_EP)
class JournalTitle(Resource):
    def get(self):
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            PUBLISHER_RESP: PUBLISHER
        }


@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, getting, reading, updating
    and deleting people.
    """
    def get(self):
        """
        The `get()` method returns a dictionary of people from the journal.
        """
        return ppl.get_people()


@api.route(f'{PEOPLE_EP}/<_id>')
class PersonDelete(Resource):
    """
    This class handles the deletion of people.
    """
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, _id):
        """
        The `delete()` method returns the deleted result.
        """
        ret = ppl.delete_person(_id)
        if ret is not False:
            return {f'Deleted {_id}': ret}
        else:
            raise wz.NotFound(f'No such person: {_id}')
