from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import werkzeug.exceptions as wz
import data.people as ppl
import data.text as text
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
TEXT_EP = '/text'


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
        """
        Retrieve jounal info including title, editor, and publisher
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            PUBLISHER_RESP: PUBLISHER
        }


@api.route(TEXT_EP)
class JournalText(Resource):
    def get(self):
        """
        Retrieve journal text
        """
        return text.read()


@api.route(f'{TEXT_EP}/<key>')
class Text(Resource):
    def get(self, key):
        """Returns specific page dictionary from given key."""
        page = text.read_one(key)
        if page:
            return page
        else:
            raise (f"No such record: {key}")

    def delete(self, key):
        """
        Deletes page from text dictionary.
        """
        ret = text.delete(key)
        if ret is not False:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such key: {key}')


@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self):
        """
        Retrieve the journal people.
        """
        return ppl.read()


@api.route(f'{PEOPLE_EP}/<_id>')
class Person(Resource):
    """
    This class handles creating, getting, reading, updating
    and deleting people.
    """
    def get(self, _id):
        """
        Retrieve a journal person.
        """
        person = ppl.read_one(_id)
        if person:
            return person
        else:
            raise wz.NotFound(f'No such record: {_id}')

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such person.')
    def delete(self, _id):
        ret = ppl.delete(_id)
        if ret is not False:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {_id}')


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLE: fields.String
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
        data = request.json
        try:
            name = data.get(ppl.NAME)
            affiliation = data.get(ppl.AFFILIATION)
            email = data.get(ppl.EMAIL)
            role = data.get(ppl.ROLE)

            ret = ppl.create(name, affiliation, email, role)

            return {
                        MESSAGE: 'Person added!',
                        RETURN: ret,
                    }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')


@api.route(f'{PEOPLE_EP}/update/<current_email>')
class PersonUpdate(Resource):
    """
    This class updates an existing person in the journal database.
    """
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable.')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self, current_email):
        """
        Update the person with the provided email, return the updated person.
        """
        data = request.json
        try:
            name = data.get('name')
            affiliation = data.get('affiliation')
            new_email = data.get('new email')
            role = data.get('role')
            ret = ppl.update(current_email, name, affiliation, new_email, role)
            return {
                MESSAGE: 'Person updated!',
                RETURN: ret
            }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: mh.get_masthead()}
