from flask import jsonify, Blueprint, url_for

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

from passlib.apps import custom_app_context as pwd_context

from application import models

from application import (
    db, JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt
)

client_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float
}

client_request_parser = reqparse.RequestParser()
client_request_parser.add_argument(
    'name',
    required=True,
    help='No name provided'
    )
client_request_parser.add_argument(
    'address',
    required=True,
    help='No address provided'
    )
client_request_parser.add_argument(
    'latitude'
    )
client_request_parser.add_argument(
    'longitude'
    )

class Client(Resource):
    def __init__(self):
        self.reqparse = client_request_parser
        super().__init__()
    
    @marshal_with(client_fields)
    def get(self, id):
        client = models.Client.query.filter_by(id=id).one()
        return client
        
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Client.query.filter_by(id=id).update(args)
        db.session.commit()
        return (id, 200, {'Location' : url_for('resources.clients.client', id=id)})
        
    def delete(self, id):
        query = models.Client.query.filter_by(id=id).one()
        db.session.delete(query)
        db.session.commit()
        return ('', 204, {'Location' : url_for('resources.clients.clients')})

class Clients(Resource):
    def __init__(self):
        self.reqparse = client_request_parser
        super().__init__()

    def get(self):
        clients = [marshal(client, client_fields) for
                    client in models.Client.query.all()]
        return {'clients' : clients}
        
    def post(self):
        args = self.reqparse.parse_args()
        client = models.Client(**args)
        db.session.add(client)
        db.session.commit()
        location = url_for('resources.clients.client', id=client.id)
        return (client.id, 201, {
            'Location':location
        })
        
clients_api = Blueprint('resources.clients', __name__)
api = Api(clients_api)
api.add_resource(
    Client,
    '/api/v1/client/<int:id>',
    endpoint='client'
    )
api.add_resource(
    Clients,
    '/api/v1/clients',
    endpoint='clients'
    )