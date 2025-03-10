from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import jsonify

def handle_validation_error(error):
    """Handle validation errors from marshmallow schemas."""
    if isinstance(error, ValidationError):
        return jsonify({
            'error': 'Validation Error',
            'messages': error.messages
        }), 400
    elif isinstance(error, IntegrityError):
        return jsonify({
            'error': 'Database Integrity Error',
            'message': 'A database constraint was violated.'
        }), 409
    elif isinstance(error, SQLAlchemyError):
        return jsonify({
            'error': 'Database Error',
            'message': 'An error occurred while accessing the database.'
        }), 500
    else:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(error)
        }), 500 