from flask import jsonify, Blueprint, url_for

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

from passlib.apps import custom_app_context as pwd_context

from application import models

from application import (
    db, JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt
)

driver_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String
}

class RegisterDriver(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided'
            )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided'
            )
        self.reqparse.add_argument(
            'vehicle_id',
            required=True,
            help='No vehicle provided'
            )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided'
            )
        super().__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        driver_data={}
        driver_data['email']=args['email']
        driver_data['name']=args['name']
        driver_data['vehicle_id']=args['vehicle_id']
        newdriver = models.Driver(**driver_data)
        db.session.add(newdriver)
        db.session.flush()
        driver = models.Driver.query.filter_by(email=args['email']).one()
        password_hash = pwd_context.hash(args['password'])
        driverauth = models.DriverAuth(driver=driver, password_hash=password_hash)
        db.session.add(driverauth)
        db.session.commit()
        location = url_for('resources.drivers.driver', id=driver.id)
        return (driver.id, 201, {
            'Location':location
        })
        
class LoginDriver(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided'
            )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided'
            )
        super().__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        try:
            driver = models.Driver.query.filter_by(email=args['email']).one()
        except:
            return 'theres no user with this email'
        if pwd_context.verify(args['password'], driver.auth.password_hash):
            access_token = create_access_token(identity=driver.id)
            print(access_token)
            return {'access_token':access_token}, 200
        return 'wrong password'
        

class Driver(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No name provided'
            )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided'
            )
        super().__init__()
    
    @marshal_with(driver_fields)
    def get(self, id):
        driver = models.Driver.query.filter_by(id=id).one()
        return driver
        
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Driver.query.filter_by(id=id).update(args)
        db.session.commit()
        return (id, 200, {'Location' : url_for('resources.drivers.driver', id=id)})
        
    def delete(self, id):
        query = models.Driver.query.filter_by(id=id).one()
        queryauth = models.DriverAuth.query.filter_by(driver_id=query.id).one()
        db.session.delete(queryauth)
        db.session.delete(query)
        db.session.commit()
        return ('', 204, {'Location' : url_for('resources.drivers.drivers')})

class Drivers(Resource):
    def get(self):
        drivers = [marshal(driver, driver_fields) for
                    driver in models.Driver.query.all()]
        return {'drivers' : drivers}
        
drivers_api = Blueprint('resources.drivers', __name__)
api = Api(drivers_api)
api.add_resource(
    Driver,
    '/api/v1/driver/<int:id>',
    endpoint='driver'
    )
api.add_resource(
    Drivers,
    '/api/v1/drivers',
    endpoint='drivers'
    )
api.add_resource(
    RegisterDriver,
    '/api/v1/registerdriver',
    endpoint='registerdriver'
    )
api.add_resource(
    LoginDriver,
    '/api/v1/logindriver',
    endpoint='logindriver'
    )