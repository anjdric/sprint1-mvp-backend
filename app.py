from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful_swagger_3 import Api, get_swagger_blueprint
from flask_jwt_extended import JWTManager

from resources.auth_resource import AuthToken
from resources.hotel_resource import Hoteis, Hotel
from resources.register_resource import Register
from resources.user_resource import User, Users

from blacklist import BLACKLIST

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'PCPi'
app.config['JWT_BLACK_ENABLE'] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)

security = [
    {
        "api_key": [],
        "Bearer": []
    }
]

authorizations = {
    "api_key": {
        "description": "Header de Autorização ApiKey usando o esquema Basic. Exemplo: \"Authorization: Basic {token}\"",
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "scheme": "Basic",
        "bearerFormat": "JWT"
    },
    "Bearer": {
        "type": "apiKey",
        "description": "Header de Autorização JWT usando o esquema Bearer. Exemplo: \"Authorization: Bearer {token}\"",
        "name": "Authorization",
        "in": "header"
    }
}

servers = [
    {
        "url": "http://localhost:5001",
        "description": "Developer Server",
    },
    {
        "url": "http://localhost:5002",
        "description": "Homolog Server",
    }
]
api = Api(app, version='1', servers=servers, title="v1 API", authorizations=authorizations,
          description='MVP API | Roteiro de Hospedagem')

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

swagger_blueprint = get_swagger_blueprint(
    api.open_api_object,
    swagger_prefix_url=SWAGGER_URL,
    swagger_url=API_URL)

# swagger.auth = auth
jwt = JWTManager(app)


@app.before_request
def initialize_database():
    database.create_all()


@jwt.token_in_blocklist_loader
def verify_token_blacklist(self, token):
    return token['jti'] in BLACKLIST


# Using the expired_token_loader decorator, we will now call
# this function whenever an expired but otherwise valid access
# token attempts to access an endpoint
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has expired'}), 403


api.add_resource(AuthToken, '/api/authenticate')
api.add_resource(Register, '/api/user/<int:user_id>')

api.add_resource(Users, '/api/users')
api.add_resource(User, '/api/users/<int:user_id>')

api.add_resource(Hoteis, '/api/hotels')
api.add_resource(Hotel, '/api/hotels/<int:hotel_id>')

app.register_blueprint(swagger_blueprint)

if __name__ == '__main__':
    from sql_alchemy import database

    database.init_app(app)
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5001)
