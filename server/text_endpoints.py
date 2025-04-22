from flask import request
from flask_restx import Resource, Namespace, fields
import data.text as txt
import werkzeug.exceptions as wz

# Create a namespace instead of a Flask app
api = Namespace('text', description='Text operations')
MESSAGE = 'Message'
RETURN = 'Return'
TEXT_EP = '/text'


@api.route('/')
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


@api.route('/<key>')
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
