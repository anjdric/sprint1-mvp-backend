from enum import Enum
from flask_restful_swagger_3 import Schema

"""
Global Resource Object Schema
"""


class NoContentSchema(Schema):
    properties = {
    }


class MessageSchema(Schema):
    type = 'object'
    properties = {
        'message': {
            'type': 'string'
        }
    }


class GlobalRequired(Enum):
    DEFAULT = 'The field is required.'

