from flask import jsonify, Blueprint, url_for

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

from passlib.apps import custom_app_context as pwd_context

from application import models

from application import (
    db, JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt
)

#Define the fields for marshalling
vehicle_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'icon': fields.String,
    'capacity': fields.Integer
}

#Define the request parser, adding each argument at a time
vehicle_request_parser = reqparse.RequestParser()
vehicle_request_parser.add_argument(
    'name',
    required=True,
    help='No name provided'
    )
vehicle_request_parser.add_argument(
    'icon'
    )
vehicle_request_parser.add_argument(
    'capacity',
    required=True,
    help='No capacity provided'
    )

class Vehicle(Resource):
    def __init__(self):
        self.reqparse = vehicle_request_parser
        super().__init__()
    
    @marshal_with(vehicle_fields)
    def get(self, id):
        vehicle = models.Vehicle.query.filter_by(id=id).one()
        return vehicle
    
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Vehicle.query.filter_by(id=id).update(args)
        db.session.commit()
        return (id, 200, {'Location' : url_for('resources.vehicles.vehicle', id=id)})
        
    def delete(self, id):
        query = models.Vehicle.query.filter_by(id=id).one()
        db.session.delete(query)
        db.session.commit()
        return ('', 204, {'Location' : url_for('resources.vehicles.vehicles')})

class Vehicles(Resource):
    def __init__(self):    
        self.reqparse = vehicle_request_parser
        super().__init__()
    
    def get(self):
        vehicles = [marshal(vehicle, vehicle_fields) for
                    vehicle in models.Vehicle.query.all()]
        return {'vehicles' : vehicles}
    
    @marshal_with(vehicle_fields)   
    def post(self):
        args = self.reqparse.parse_args()
        vehicle = models.Vehicle(**args)
        db.session.add(vehicle)
        db.session.commit()
        location = url_for('resources.vehicles.vehicle', id=vehicle.id)
        return (vehicle, 201, {
            'Location':location
        })
        
vehicles_api = Blueprint('resources.vehicles', __name__)
api = Api(vehicles_api)
api.add_resource(
    Vehicle,
    '/api/v1/vehicle/<int:id>',
    endpoint='vehicle'
    )
api.add_resource(
    Vehicles,
    '/api/v1/vehicles',
    endpoint='vehicles'
    )