# import Infrastructure
import traceback
from http import HTTPStatus as _

# import framework
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger, Resource
from werkzeug.exceptions import BadRequest

# import schema
from models.hotel import HotelModel
from schema.global_schema import MessageSchema
from schema.hotel_schema import HotelSchema, HotelRequired as REQUIRED


@swagger.tags('Hoteis')
class Hoteis(Resource):
    # Global variable of filter hotel parameters
    query_params = reqparse.RequestParser()
    query_params.add_argument("cidade", type=str, default=None, location="args")
    query_params.add_argument("estrelas_min", type=float, default=0, location="args")
    query_params.add_argument("estrelas_max", type=float, default=5, location="args")
    query_params.add_argument("diaria_min", type=float, default=0, location="args")
    query_params.add_argument("diaria_max", type=float, default=10000, location="args")
    query_params.add_argument("limit", type=float, default=25, location="args")
    query_params.add_argument("offset", type=float, default=1, location="args")

    # Global variable of domain hotel parameters
    post_args = reqparse.RequestParser()
    post_args.add_argument("user_id", type=int, required=True, help=REQUIRED.USER_ID.value)
    post_args.add_argument("nome", type=str, required=True, help=REQUIRED.NOME.value)
    post_args.add_argument("estrelas", type=float, required=True, help=REQUIRED.ESTRELAS.value)
    post_args.add_argument("diaria", type=float, required=True, help=REQUIRED.DIARIA.value)
    post_args.add_argument("cidade", type=str, required=True, help=REQUIRED.CIDADE.value)
    post_args.add_argument("uf", type=str, required=True, help=REQUIRED.UF.value)
    post_args.add_argument("url_image", type=str, required=False)
    post_args.add_argument("url_background", type=str, required=False)
    post_args.add_argument("url_youtube", type=str, required=False)
    post_args.add_argument("url_instagran", type=str, required=False)
    post_args.add_argument("url_facebook", type=str, required=False)

    @swagger.reorder_list_with(HotelSchema, summary="*** Return a List of Hotels")
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def get(self):
        """Returns all Hotels.
        """
        try:
            dados = self.query_params.parse_args()
            query = HotelModel.query
            if dados.get("cidade"):
                query = query.filter(HotelModel.cidade.like(f'%{dados["cidade"]}%'))

            hotels = query.filter(
                HotelModel.estrelas >= dados["estrelas_min"],
                HotelModel.estrelas <= dados["estrelas_max"],
                HotelModel.diaria >= dados["diaria_min"],
                HotelModel.diaria <= dados["diaria_max"]) \
                .paginate(page=dados["offset"], per_page=dados["limit"])

            return list(map(lambda hotel: HotelSchema(**hotel.json()), hotels)), _.OK
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(MessageSchema, response_code=_.CREATED, summary="Register a New Hotel")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    @swagger.reqparser(name='RegisterHotelSchema', parser=post_args)
    def post(self):
        """Create hotel.
        """
        try:
            print(self.post_args)
            dados = self.post_args.parse_args()
            if not dados.get('nome') or dados is None:
                return MessageSchema(**{"message": f"The field 'nome' is required"}), _.BAD_REQUEST

            if not dados.get('estrelas') or dados is None:
                return MessageSchema(**{"message": f"The field 'estrelas' is required"}), _.BAD_REQUEST

            if not dados.get('diaria') or dados is None:
                return MessageSchema(**{"message": f"The field 'diaria' is required"}), _.BAD_REQUEST

            if not dados.get('cidade') or dados is None:
                return MessageSchema(**{"message": f"The field 'cidade' is required"}), _.BAD_REQUEST

            if not dados.get('uf') or dados is None:
                return MessageSchema(**{"message": f"The field 'uf' is required"}), _.BAD_REQUEST

            if not dados.get('user_id') or dados is None:
                return MessageSchema(**{"message": f"The field 'user_id' is required"}), _.BAD_REQUEST

            if HotelModel.find_by_nome(dados['nome']):
                return MessageSchema(**{"message": f"Hotel with nome '{dados['nome']}' already exists."}), _.BAD_REQUEST

            hotel = HotelModel(**dados)
            hotel.save_hotel()
            return MessageSchema(**{"message": "Hotel created successfully."}), _.CREATED
        except BadRequest as e:
            print(e)
            return MessageSchema(**{"message": f"{e}"}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR


@swagger.tags('Hoteis')
class Hotel(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument("user_id", type=int, required=True, help=REQUIRED.USER_ID.value)
    post_args.add_argument("nome", type=str, required=True, help=REQUIRED.NOME.value)
    post_args.add_argument("estrelas", type=float, required=True, help=REQUIRED.ESTRELAS.value)
    post_args.add_argument("diaria", type=float, required=True, help=REQUIRED.DIARIA.value)
    post_args.add_argument("cidade", type=str, required=True, help=REQUIRED.CIDADE.value)
    post_args.add_argument("uf", type=str, required=True, help=REQUIRED.UF.value)
    post_args.add_argument("url_image", type=str, required=False)
    post_args.add_argument("url_background", type=str, required=False)
    post_args.add_argument("url_youtube", type=str, required=False)
    post_args.add_argument("url_instagran", type=str, required=False)
    post_args.add_argument("url_facebook", type=str, required=False)

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(HotelSchema, summary="*** Search Hotel By Identifier.")
    @swagger.response(schema=MessageSchema, response_code=_.NOT_FOUND, description=_.NOT_FOUND.description)
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def get(self, hotel_id):
        """ Return Hotel By Identifier.
        """
        try:
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                return HotelSchema(**hotel.json()), _.OK
            return MessageSchema(**{'message': 'Hotel not found'}), _.NOT_FOUND
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(schema=HotelSchema, summary="Update Registration")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    @swagger.reqparser(name='UpdateHotelSchema', parser=post_args)
    def put(self, hotel_id):
        """ Updated Registration
        """
        try:
            dados = self.post_args.parse_args()

            if dados is None:
                return {"message": f"hotel not found!"}, _.BAD_REQUEST

            hotel = HotelModel.find_hotel(hotel_id)
            if not hotel:
                return MessageSchema(**{"message": f"edit hotel:{_.BAD_REQUEST.description}."}), _.BAD_REQUEST

            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return HotelSchema(**hotel.json()), _.OK
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR

    @jwt_required()
    @swagger.security(Bearer=[])
    @swagger.reorder_with(MessageSchema, summary="*** Remove hotel from the Database")
    @swagger.response(schema=MessageSchema, response_code=_.BAD_REQUEST, description=_.BAD_REQUEST.description)
    @swagger.response(schema=MessageSchema, response_code=_.INTERNAL_SERVER_ERROR, description=_.INTERNAL_SERVER_ERROR.description)
    def delete(self, hotel_id):
        """ Deleted Hotel.
        """
        try:
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                hotel.delete_hotel()
                return MessageSchema(**{'message': 'Deleted'}), _.OK
            return MessageSchema(**{"message": f"Deleted hotel: {_.BAD_REQUEST.description}."}), _.BAD_REQUEST
        except BadRequest as e:
            return MessageSchema(**{e.data['message']['name']}), _.BAD_REQUEST
        except Exception as e:
            print(e)
            traceback.print_exc()
            return MessageSchema(**{"message": f"{_.INTERNAL_SERVER_ERROR.description}."}), _.INTERNAL_SERVER_ERROR
