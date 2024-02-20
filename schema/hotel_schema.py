from enum import Enum
from flask_restful_swagger_3 import Schema

"""
Hotel Resource Object Schema
"""


class HotelIdSchema(Schema):
    type = 'object'
    properties = {
        'hotel_id': {
            'type': 'integer',
            'format': 'int64',
        }
    }
    required = ['hotel_id']


class HotelSchema(HotelIdSchema):
    properties = {
        'nome': {
            'type': 'string',
            'nullable': False
        },
        'estrelas': {
            'type': 'float',
            'nullable': False
        },
        'diaria': {
            'type': 'float',
            'nullable': False
        },
        'cidade': {
            'type': 'string',
            'nullable': False
        },
        'uf': {
            'type': 'string',
            'nullable': False
        },
        'url_image': {
            'type': 'string',
            'nullable': True
        },
        'url_background': {
            'type': 'string',
            'nullable': True
        },
        'url_youtube': {
            'type': 'string',
            'nullable': True
        },
        'url_instagran': {
            'type': 'string',
            'nullable': True
        },
        'url_facebook': {
            'type': 'string',
            'nullable': True
        },
        'active': {
            'type': 'bool',
            'nullable': False
        },
        'checked': {
            'type': 'bool',
            'nullable': False
        },
        'user_id': {
            'type': 'integer',
            'nullable': False,
            'format': 'int64'
        }
    }
    # required = ['nome']
    # required = ['estrelas']


""" 
Specifications Validation 
"""


class HotelRequired(Enum):
    NOME = 'The field \'Nome\' is required.'
    ESTRELAS = 'The field \'Estrelas\' is required.'
    DIARIA = 'The field \'Diaria\' is required.'
    CIDADE = 'The field \'Cidade\' is required.'
    ACTIVE = 'The field \'Active\' is required.'
    CHECKED = 'The field \'Checked\' is required.'
    UF = 'The field \'UF\' is required.'
    USER_ID = 'The field \'User Id\' is required.'
