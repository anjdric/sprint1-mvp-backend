# import Infrastructure
from http import HTTPStatus as _
from hmac import compare_digest

# import framework
from flask_restful import reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from flask_restful_swagger_3 import swagger, Resource

# import schema
from blacklist import BLACKLIST
from models.user import UsuarioModel
from schema.global_schema import MessageSchema
from schema.user_schema import TokenSchema


@swagger.tags('Session Token')
class AuthToken(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument("username", type=str, required=True, help="The field 'login' is required.")
    post_args.add_argument("password", type=str, required=True, help="The field 'password' is required.")

    @swagger.reorder_with(TokenSchema, summary="*** Create a Session Token ")
    @swagger.response(schema=MessageSchema, response_code=_.FORBIDDEN, description=_.FORBIDDEN.description)
    @swagger.response(schema=MessageSchema, response_code=_.UNAUTHORIZED, description=_.UNAUTHORIZED.description)
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    @swagger.reqparser(name='AuthenticateModel', parser=post_args)
    def post(self):
        """ Receives Authentication Data and Returns a New Session Token
        """
        try:
            dados = self.post_args.parse_args()
            user = UsuarioModel.find_by_login(dados['username'])

            if user and compare_digest(user.password, dados['password']):
                if user.active:
                    access_token = create_access_token(identity=user.user_id, fresh=True)
                    refresh_token = create_refresh_token(user.user_id)
                    return TokenSchema(
                        **{"token_type": "Bearer", "access_token": access_token, "refresh_token": refresh_token}), _.OK
                else:
                    """ User not confirmed. """
                    return MessageSchema(**{'message': 'User not confirmed.'}), _.FORBIDDEN
                """ The username or password is incorrect. """
            return MessageSchema(**{"message": f"The username or password is incorrect."}), _.UNAUTHORIZED
        except BadRequest as e:
            return e.data, _.BAD_REQUEST
        except Exception as e:
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(TokenSchema, summary="*** Refresh a Session Token. *** NOTE: Token can only be updated once")
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def put(self):
        """ Receives a Token and Returns and Refresh a Session Token.  *** NOTE: Token can only be updated once
        """
        try:
            current_user = get_jwt_identity()
            new_token = create_access_token(identity=current_user, fresh=False)
            # Make it clear that when to add the refresh token to the blocklist will depend on the app design
            jti = get_jwt()["jti"]
            BLACKLIST.add(jti)
            return TokenSchema(**{"token_type": "Bearer", "access_token": new_token, "refresh_token": ''}), _.OK
        except Exception as e:
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(MessageSchema, summary="*** Remove a Session Token")
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def delete(self):
        """ Remove Current Session Token
        """
        try:
            jwt_id = get_jwt()['jti']  # JWT Token Identifier
            BLACKLIST.add(jwt_id)
            return MessageSchema(**{"message": f"Logged out successfully."}), _.OK
        except Exception as e:
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR
