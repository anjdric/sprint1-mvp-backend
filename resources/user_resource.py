# import Infrastructure
import traceback
from http import HTTPStatus as _
from hmac import compare_digest

# import framework
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger, Resource
from werkzeug.exceptions import BadRequest

# import schema
from models.user import UsuarioModel
from schema.global_schema import MessageSchema
from schema.user_schema import UserModelSchema, UserRequired as REQUIRED


@swagger.tags('Users')
class Users(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument("name", type=str, required=True, help=REQUIRED.NAME.value)
    post_args.add_argument("login", type=str, required=True, help=REQUIRED.LOGIN.value)
    post_args.add_argument("password", type=str, required=True, help=REQUIRED.PASSWORD.value)
    post_args.add_argument("email", type=str, required=True, help=REQUIRED.EMAIL.value)

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_list_with(UserModelSchema, summary="*** Return a List of Users")
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def get(self):
        """Returns all users.
        """
        try:
            users = [user.json() for user in UsuarioModel.query.all()]
            return list(map(lambda user: UserModelSchema(**user), users)), _.OK
        except Exception as e:
            print(e)
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @swagger.reorder_with(MessageSchema, response_code=_.CREATED, summary="Register a New User")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    @swagger.reqparser(name='RegisterUserSchema', parser=post_args)
    def post(self):
        """ Created: Registered
        """
        try:
            dados = self.post_args.parse_args()
            if not dados.get('email') or dados is None:
                return MessageSchema(**{"message": f"he field 'email' is required."}), _.BAD_REQUEST

            if UsuarioModel.find_by_email(dados['email']):
                return MessageSchema(**{"message": f"Email '{dados['email']}' already exists."}), _.BAD_REQUEST

            if UsuarioModel.find_by_login(dados['login']):
                return MessageSchema(**{"message": f"User '{dados['login']}' already exists."}), _.BAD_REQUEST

            user = UsuarioModel(**dados)
            user.save_user()
            # user.send_confirmation_email()
            return MessageSchema(**{"message": "User created successfully."}), _.CREATED
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR


@swagger.tags('Users')
@swagger.security(Bearer=[])
class User(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument("name", type=str, required=True, help=REQUIRED.NAME.value)
    post_args.add_argument("login", type=str, required=True, help=REQUIRED.LOGIN.value)
    post_args.add_argument("password", type=str, required=True, help=REQUIRED.PASSWORD.value)
    post_args.add_argument("email", type=str, required=True, help=REQUIRED.EMAIL.value)

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(UserModelSchema, summary="*** Search User By Identifier.")
    @swagger.response(schema=MessageSchema, response_code=_.NOT_FOUND, description=_.NOT_FOUND.description)
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def get(self, user_id):
        """ Return User By Identifier.
        """
        try:
            user = UsuarioModel.find_user(user_id)
            if user:
                return UserModelSchema(**user.json()), _.OK
            return MessageSchema(**{'message': 'user not found'}), _.NOT_FOUND
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(schema=UserModelSchema, summary="Update Registration")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    @swagger.reqparser(name='UserSchema', parser=post_args)
    def put(self, user_id):
        """ Updated Registration
        """
        try:
            dados = self.post_args.parse_args()

            if not dados.get('password') or dados is None:
                return {"message": f"he field 'password' is required."}, _.BAD_REQUEST

            user = UsuarioModel.find_user(user_id)
            if not user:
                return MessageSchema(**{"message": f"edit user:{_.BAD_REQUEST.description}."}), _.BAD_REQUEST

            user_outer = UsuarioModel.find_by_email(dados['email'])
            if user_outer and user_outer.user_id != user.user_id:
                return MessageSchema(**{"message": f"Email '{dados['email']}' already exists."}), _.BAD_REQUEST

            user_outer = UsuarioModel.find_by_login(dados['login'])
            if user_outer and user_outer.user_id != user.user_id:
                return MessageSchema(**{"message": f"User '{dados['login']}' already exists."}), _.BAD_REQUEST

            if not compare_digest(user.password, dados['password']):
                return MessageSchema(**{"message": "Login or Password do not Match"}), _.BAD_REQUEST

            user.update_user(**dados)
            user.save_user()
            return UserModelSchema(**user.json()), _.OK
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(MessageSchema, summary="*** Remove user from the Database")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def delete(self, user_id):
        """ Deleted User.
        """
        try:
            user = UsuarioModel.find_user(user_id)
            if user:
                user.delete_user()
                return MessageSchema(**{'message': 'Deleted'}), _.OK
            return MessageSchema(**{"message": f"Deleted user: {_.BAD_REQUEST.description}."}), _.BAD_REQUEST
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR
