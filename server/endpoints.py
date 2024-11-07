from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import werkzeug.exceptions as wz
import data.people as ppl
import data.masthead as mh
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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
MESSAGE = 'Message'
PEOPLE_EP = '/people'
PUBLISHER = 'FirstClass'
PUBLISHER_RESP = 'Publisher'
RETURN = 'Return'
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
        return ppl.get()


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
        ret = ppl.delete(_id)
        if ret is not False:
            return {f'Deleted {_id}': ret}
        else:
            raise wz.NotFound(f'No such person: {_id}')


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String
})


@api.route(f'{PEOPLE_EP}/create')
class PersonCreate(Resource):
    """
    This class adds a person to the journal database.
    """
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable.')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person, return the added person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            ret = ppl.create(name, affiliation, email)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: mh.get_masthead()}
