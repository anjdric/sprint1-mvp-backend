from enum import Enum
from flask_restful_swagger_3 import Schema

"""
User Resource Object Schema
"""





class AuthenticateSchema(Schema):
    type = 'object'
    properties = {
        'login': {
            'type': 'string',
            'nullable': False
        },
        'password': {
            'type': 'string',
            'nullable': False
        },
        'email': {
            'type': 'string',
            'nullable': True
        }
    }
    required = ['login', 'password']


class TokenSchema(Schema):
    properties = {
        'token_type': {
            'type': 'string',
            'default': 'Bearer'
        },
        'access_token': {
            'type': 'string'
        },
        'refresh_token': {
            'type': 'string'
        }
    }


class UserIdModelSchema(Schema):
    type = 'object'
    properties = {
        'user_id': {
            'type': 'integer',
            'format': 'int64',
        }
    }
    required = ['user_id']


class UserModelSchema(UserIdModelSchema):
    properties = {
        'name': {
            'type': 'string',
            'nullable': False
        },
        'login': {
            'type': 'string',
            'nullable': False
        },
        'email': {
            'type': 'string',
            'nullable': False
        },
        'active': {
            'type': 'boolean',
            'nullable': True
        }
    }
    required = ['login']
    required = ['email']


""" 
Specifications Validation 
"""


class UserRequired(Enum):
    NAME = 'The field \'Nome\' is required.'
    EMAIL = 'The field \'Email\' is required.'
    LOGIN = 'The field \'Login\' is required.'
    PASSWORD = 'The field \'Password\' is required.'
