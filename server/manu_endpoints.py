from http import HTTPStatus
from flask import request
from flask_restx import Resource, Namespace, fields
import data.manuscripts as manu
import data.manus.query as query
import data.db_connect as dbc
import data.people as ppl
import werkzeug.exceptions as wz

# Create a namespace instead of a Flask app
api = Namespace('manuscripts', description='Manuscript operations')
MESSAGE = 'Message'
RETURN = 'Return'


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


@api.route('/')
class GetManuscripts(Resource):
    """fetch all manuscripts"""

    def get(self):
        """fetch the manuscripts"""
        return manu.read()


@api.route('/<author>')
class GetManuscriptsByAuthor(Resource):
    """fetch manuscripts by author"""
    def get(self, author):
        """
        Fetch manuscripts by author.
        Args:
            author: str - Email of the author
        Returns:
            list: List of manuscripts by the author
        """
        return manu.get_manuscript(author)


@api.route('/receive_action')
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
                ref = data.get('referee')
                if not ref:
                    raise ValueError("Referee email required for referee")
                kwargs['ref'] = ref
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


@api.route('/delete/<string:_id>')
class DeleteManuscript(Resource):
    """
    Delete a manuscript by ID.
    """
    @api.response(HTTPStatus.OK, 'Success.')
    @api.response(HTTPStatus.NOT_FOUND, 'No such manuscript.')
    def delete(self, _id):
        """
        Delete a manuscript by ID.
        """
        ret = manu.delete_manuscript(_id)
        if ret != 0:
            return {'Deleted': ret}
        else:
            raise wz.NotFound(f'No such manuscript: {_id}')


@api.route('/create')
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

            # Check if author email exists in people collection
            if ppl.exists(author):
                # Get the person
                person = ppl.read_one(author)

                # Check if person already has the 'AU' role
                if 'AU' not in person.get(ppl.ROLES, []):
                    # Add 'AU' role to the person
                    current_roles = person.get(ppl.ROLES, [])
                    current_roles.append('AU')

                    # Update the person with the new role
                    ppl.update(
                        author,
                        person.get(ppl.NAME),
                        person.get(ppl.AFFILIATION),
                        author,
                        current_roles
                    )

            return {
                MESSAGE: 'Manuscript created successfully!',
                RETURN: manu_id,
            }
        except Exception as err:
            raise wz.NotAcceptable(f'Failed to create manuscript: {str(err)}')


@api.route('/state_transitions')
class ManuscriptStateTransitions(Resource):
    def get(self):
        """
        Return a mapping of state codes to valid actions.
        """
        transitions = {}
        for state in query.VALID_STATES:
            transitions[state] = list(query.get_valid_actions_by_state(state))
        return transitions


@api.route('/state_names')
class ManuscriptStateNames(Resource):
    def get(self):
        """Return a mapping of state codes to their human-readable names."""
        # Map state and action codes to human-readable names
        state_names = {
            # States
            query.SUBMITTED: 'Submitted',
            query.AUTHOR_REVIEW: 'Author Review',
            query.COPY_EDIT: 'Copy Editing',
            query.EDITOR_REVIEW: 'Editor Review',
            query.FORMATTING: 'Formatting',
            query.IN_REF_REV: 'In Referee Review',
            query.PUBLISHED: 'Published',
            query.REJECTED: 'Rejected',
            query.WITHDRAWN: 'Withdrawn',
            # Actions
            query.ASSIGN_REF: 'Assign Referee',
            query.DELETE_REF: 'Delete Referee',
            query.ACCEPT: 'Accept',
            query.DONE: 'Done',
            query.EDITOR_MOVE: 'Editor Move',
        }
        return state_names


@api.route('/valid_states')
class ManuscriptValidStates(Resource):
    def get(self):
        """Return valid states with their display names

        Returns:
            list: List of dictionaries with state codes and names
        """
        state_names = {
            query.SUBMITTED: 'Submitted',
            query.EDITOR_REVIEW: 'Editor Review',
            query.FORMATTING: 'Formatting',
            query.IN_REF_REV: 'In Referee Review',
            query.PUBLISHED: 'Published',
            query.REJECTED: 'Rejected',
            query.WITHDRAWN: 'Withdrawn',
            query.COPY_EDIT: 'Copy Editing',
            query.AUTHOR_REVIEW: 'Author Review',
        }
        # Return a list of objects with code and name for each state
        valid_states = []
        for s in query.VALID_STATES:
            valid_states.append({'code': s, 'name': state_names.get(s, s)})
        return valid_states


@api.route('/sorted')
class ManuscriptSorted(Resource):
    def get(self):
        """Return all manuscripts sorted by their state in the workflow."""
        sorted_manuscripts = manu.sort_manuscripts_by_state()

        # Convert MongoDB ObjectIDs to strings for JSON serialization
        for manuscript in sorted_manuscripts:
            dbc.convert_mongo_id(manuscript)

        return sorted_manuscripts


@api.route('/state/<string:state>')
class ManuscriptsByState(Resource):
    def get(self, state):
        """Return manuscripts filtered by a specific state.
        Args:
            state: The state code to filter by (e.g., 'SUB', 'PUB')
        Returns:
            List of manuscripts in the specified state
        """
        try:
            filtered_manuscripts = manu.filter_manuscripts_by_state(state)

            # Convert MongoDB ObjectIDs to strings for JSON serialization
            for manuscript in filtered_manuscripts:
                dbc.convert_mongo_id(manuscript)

            return filtered_manuscripts
        except ValueError as e:
            return {'error': str(e)}, 400
