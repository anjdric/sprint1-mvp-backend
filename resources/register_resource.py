# import Infrastructure
import traceback
from http import HTTPStatus as _
from hmac import compare_digest

# import framework
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger, Resource
from werkzeug.exceptions import BadRequest

from models.user import UsuarioModel
from schema.global_schema import MessageSchema


@swagger.tags('ConfirmAccount')
class Register(Resource):
    @swagger.reorder_with(MessageSchema, summary="Confirm Registration.")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def get(self, user_id):
        """Ok: Registration Confirmed"""
        user = UsuarioModel.find_user(user_id)
        if not user:
            return MessageSchema(**{'message': _.NOT_FOUND.description}), _.NOT_FOUND
        user.active = True
        try:
            user.save_user()
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR
        return MessageSchema(**{'message': _.OK.description}), _.OK
        # headers = {'Content-Type': 'test/html'}
        # return make_response(render_template('user_confirm.html', email=user.email, usuario=user.login), 200)

