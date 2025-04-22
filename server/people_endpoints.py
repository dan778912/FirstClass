from http import HTTPStatus
from flask import request
from flask_restx import Resource, Namespace, fields
import data.people as ppl
import data.masthead as mh
import werkzeug.exceptions as wz

# Create a namespace instead of a Flask app
api = Namespace('people', description='People operations')
MESSAGE = 'Message'
RETURN = 'Return'
PEOPLE_EP = '/people'
REF_EP = '/referees'


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLE: fields.String,
    ppl.PASSWORD: fields.String(required=True)  # Password now required
})


@api.route('/')
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


@api.route(REF_EP)
class Referees(Resource):
    """
    Get a list of referees from the database.
    Returns:
        list: List of referee emails
    """
    def get(self):
        return ppl.get_referees()


@api.route('/<_id>')
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

    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable.')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self, _id):
        data = request.json
        try:
            name = data.get('name')
            affiliation = data.get('affiliation')
            new_email = data.get('email')
            roles = data.get('roles', [])
            if not roles:
                # For backward compatibility
                role = data.get('role')
                roles = [role] if role else []
            email = new_email if new_email else _id
            ret = ppl.update(_id, name, affiliation, email, roles)
            return {
                MESSAGE: 'Person updated!',
                RETURN: ret
            }
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: {err=}')


@api.route('/create')
class PersonCreate(Resource):
    """
    This class adds a person to the journal database.
    Password is required for direct user creation.
    """
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable.')
    @api.expect(PEOPLE_CREATE_FLDS)
    def post(self):
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


AUTH_FLDS = api.model('AuthenticateUser', {
    ppl.EMAIL: fields.String(required=True),
    ppl.PASSWORD: fields.String(required=True)
})


@api.route('/name/<email>')
class PersonName(Resource):
    def get(self, email):
        return {ppl.NAME: ppl.read_name(email)}


@api.route('/login')
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


MASTHEAD = 'Masthead'


@api.route('/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: mh.get_masthead()}
