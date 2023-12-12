# import Infrastructure
import traceback
from http import HTTPStatus as _
from hmac import compare_digest

# import framework
from flask_restful import reqparse
from flask_jwt_extended import jwt_required
from flask_restful_swagger_3 import swagger, Resource
from werkzeug.exceptions import BadRequest

from models.hotel import HotelModel
from schema.global_schema import MessageSchema
from schema.hotel_schema import HotelSchema


@swagger.tags('Hoteis')
class Hoteis(Resource):
    query_params = reqparse.RequestParser()
    query_params.add_argument("cidade", type=str, default=None, location="args")
    query_params.add_argument("estrelas_min", type=float, default=0, location="args")
    query_params.add_argument("estrelas_max", type=float, default=5, location="args")
    query_params.add_argument("diaria_min", type=float, default=0, location="args")
    query_params.add_argument("diaria_max", type=float, default=10000, location="args")
    query_params.add_argument("limit", type=float, default=25, location="args")
    query_params.add_argument("offset", type=float, default=1, location="args")

    @jwt_required()
    @swagger.security(Bearer=[])
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


@swagger.tags('Hoteis')
class Hotel(Resource):
    post_args = reqparse.RequestParser()
    post_args.add_argument("nome", type=str, required=True, help="The field 'nome' is required.")
    post_args.add_argument("estrelas")
    post_args.add_argument("diaria")
    post_args.add_argument("cidade")
    post_args.add_argument("site_id", type=int, required=True, help="The field 'site' is required.")

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


