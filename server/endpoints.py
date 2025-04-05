from http import HTTPStatus
from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS
from datetime import datetime, timezone
import werkzeug.exceptions as wz
import data.people as ppl
import data.text as txt
import data.masthead as mh
import data.manuscripts as manu
import data.manus.query as query
import data.roles as rls
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)
CORS(app)
api = Api(app)

DATE = datetime.now(timezone.utc).isoformat()  # should get the actual date
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
MANU_EP = '/manuscripts'
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


@api.route(TEXT_EP)
class JournalText(Resource):
    def get(self):
        """
        Retrieve journal text
        """
        return txt.read()


TEXT_FLDS = api.model('AddNewTextEntry', {
    # key: str, title: str, text: str
    txt.KEY: fields.String,
    txt.TITLE: fields.String,
    txt.TEXT: fields.String
})


@api.route(f'{TEXT_EP}/<key>')
class Text(Resource):
    """
    This class handles CRUD operations for text.
    """
    def get(self, key):
        """Returns specific page dictionary from given key."""
        page = txt.read_one(key)
        if page:
            return page
        else:
            raise wz.NotFound(f"No such record: {key}")

    def delete(self, key):
        """
        Deletes page from text dictionary.
        """
        ret = txt.delete(key)
        if ret is not False:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such key: {key}')

    @api.expect(TEXT_FLDS)
    def post(self, key):
        """Create a new text entry."""
        data = request.json
        try:
            title = data.get(txt.TITLE)
            text = data.get(txt.TEXT)
            ret = txt.create(key, title, text)
            return {
                        MESSAGE: 'Text added!',
                        RETURN: ret,
                    }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add text: '
                                   f'{err=}')

    @api.expect(TEXT_FLDS)
    def put(self, key):
        """Update an existing text entry."""
        data = request.json
        try:
            title = data.get(txt.TITLE)
            text = data.get(txt.TEXT)
            ret = txt.update(key, title, text)
            return {
                        MESSAGE: 'Text updated!',
                        RETURN: ret,
                    }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update text: '
                                   f'{err=}')


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
        if ret != 0:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such person: {_id}')


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLE: fields.String,
    ppl.PASSWORD: fields.String(required=True)  # Password now required
})


@api.route(f'{PEOPLE_EP}/create')
class PersonCreate(Resource):
    """
    This class adds a person to the journal database.
    Password is required for direct user creation.
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
            roles = data.get(ppl.ROLES, [])
            if not roles:
                # For backward compatibility, check single role
                role = data.get(ppl.ROLE)
                roles = [role] if role else []

            password = data.get(ppl.PASSWORD)
            if not password:
                raise ValueError("Password is required")

            ret = ppl.create(
                name, affiliation, email, roles, password=password)

            return {
                        MESSAGE: 'Person added!',
                        RETURN: ret,
                    }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')


@api.route(f'{PEOPLE_EP}/update/<current_email>')
class PersonUpdate(Resource):
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable.')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self, current_email):
        data = request.json
        print('PersonUpdate - Received data:', data)
        try:
            name = data.get('name')
            affiliation = data.get('affiliation')
            new_email = data.get('email')
            roles = data.get('roles', [])
            if not roles:
                # For backward compatibility
                role = data.get('role')
                roles = [role] if role else []
            print('PersonUpdate - Extracted roles:', roles)
            email = new_email if new_email else current_email
            ret = ppl.update(current_email, name, affiliation, email, roles)
            return {
                MESSAGE: 'Person updated!',
                RETURN: ret
            }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: {err=}')


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: mh.get_masthead()}


REFEREE_FIELDS = api.model('RefereeData', {
    'report': fields.String(required=False, description='Referee report'),
    'verdict': fields.String(required=False, description='Referee verdict')
})


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manu.MANU_ID: fields.String(required=True,
                                description='Manuscript ID'),
    manu.CURR_STATE: fields.String(required=True,
                                   description='Current state'),
    manu.ACTION: fields.String(required=True, description='Action to perform'),
    'referee': fields.String(required=False,
                             description='Referee email for referee stuff'),
    'referee_data': fields.Nested(REFEREE_FIELDS, required=False,
                                  description='Additional referee data')
})


@api.route(f'{MANU_EP}')
class GetManuscripts(Resource):
    """fetch all manuscripts"""

    def get(self):
        """fetch the manuscripts"""
        return manu.read()


@api.route(f'{MANU_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            data = request.json
            manu_id = data.get(manu.MANU_ID)
            curr_state = data.get(manu.CURR_STATE)
            action = data.get(manu.ACTION)

            # Build kwargs based on the action
            kwargs = {}
            if action in ['ARF', 'DRF']:  # Referee-related actions
                referee = data.get('referee')
                if not referee:
                    raise ValueError("Referee email required for referee")
                kwargs['referee'] = referee
                # Include referee data if provided
                if data.get('referee_data'):
                    kwargs['extra'] = data['referee_data']
            ret = manu.handle_action(manu_id, curr_state, action, **kwargs)
            return {
                MESSAGE: 'Action received!',
                RETURN: ret,
            }
        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: {str(err)}')


MANU_CREATE_FLDS = api.model('CreateManuscript', {
    manu.TITLE: fields.String,
    manu.AUTHOR: fields.String,
})


@api.route(f'{MANU_EP}/delete/<string:_id>')
class DeleteManuscript(Resource):
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such manuscript.')
    def delete(self, _id):
        ret = manu.delete_manuscript(_id)
        if ret != 0:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such manuscript: {_id}')


@api.route(f'{MANU_EP}/create')
class CreateManuscript(Resource):
    """
    Create a new manuscript.
    """
    @api.expect(MANU_CREATE_FLDS)
    def put(self):
        """
        Create a new manuscript.
        """
        try:
            title = request.json.get(manu.TITLE)
            author = request.json.get(manu.AUTHOR)
            # make referees optional
            manu.CURR_STATE = "curr_state"

            if not title or not author:
                raise ValueError("Title and author are required")

            manu_id = manu.create_manuscript(title, author)
            return {
                MESSAGE: 'Manuscript created successfully!',
                RETURN: manu_id,
            }
        except Exception as err:
            raise wz.NotAcceptable(f'Failed to create manuscript: {str(err)}')


@api.route(f'{MANU_EP}/state_transitions')
class ManuscriptStateTransitions(Resource):
    def get(self):
        transitions = {}
        for state in query.VALID_STATES:
            transitions[state] = list(manu.get_valid_actions_by_state(state))
        return transitions


AUTH_FLDS = api.model('AuthenticateUser', {
    ppl.EMAIL: fields.String(required=True),
    ppl.PASSWORD: fields.String(required=True)
})


@api.route(f'{PEOPLE_EP}/login')
class PersonLogin(Resource):
    """
    This class handles user authentication.
    """
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.UNAUTHORIZED, 'Invalid credentials.')
    @api.expect(AUTH_FLDS)
    def post(self):
        """
        Authenticate a user with email and password.
        """
        data = request.json
        try:
            email = data.get(ppl.EMAIL)
            password = data.get(ppl.PASSWORD)

            if not email or not password:
                raise ValueError("Email and password are required")

            person = ppl.authenticate(email, password)
            if person:
                return {
                    MESSAGE: 'Authentication successful',
                    RETURN: {
                        'email': person[ppl.EMAIL],
                        'name': person[ppl.NAME],
                        'roles': person[ppl.ROLES]
                    }
                }
            else:
                raise wz.Unauthorized('Invalid email or password')

        except Exception as err:
            if isinstance(err, wz.Unauthorized):
                raise
            raise wz.NotAcceptable(f'Authentication failed: {err=}')
