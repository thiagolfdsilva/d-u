from flask import jsonify, Blueprint, url_for

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

from passlib.apps import custom_app_context as pwd_context

from application import models

from application import (
    db, JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt
)

cdd_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'latitude': fields.Float,
    'longitude': fields.Float
}


cdd_request_parser = reqparse.RequestParser()
cdd_request_parser.add_argument(
    'name',
    required=True,
    help='No name provided'
    )
cdd_request_parser.add_argument(
    'address',
    required=True,
    help='No address provided'
    )
cdd_request_parser.add_argument(
    'latitude'
    )
cdd_request_parser.add_argument(
    'longitude'
    )

class CDD(Resource):
    def __init__(self):
        self.reqparse = cdd_request_parser
        super().__init__()
    
    @marshal_with(cdd_fields)
    def get(self, id):
        cdd = models.CDD.query.filter_by(id=id).one()
        return cdd
        
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.CDD.query.filter_by(id=id).update(args)
        db.session.commit()
        return (id, 200, {'Location' : url_for('resources.cdds.cdd', id=id)})
        
    def delete(self, id):
        query = models.CDD.query.filter_by(id=id).one()
        db.session.delete(query)
        db.session.commit()
        return ('', 204, {'Location' : url_for('resources.cdds.cdds')})

class CDDs(Resource):
    def __init__(self):
        self.reqparse = cdd_request_parser
        super().__init__()

    def get(self):
        cdds = [marshal(cdd, cdd_fields) for
                    cdd in models.CDD.query.all()]
        return {'cdds' : cdds}
        
    def post(self):
        args = self.reqparse.parse_args()
        cdd = models.CDD(**args)
        db.session.add(cdd)
        db.session.commit()
        location = url_for('resources.cdds.cdd', id=cdd.id)
        return (cdd.id, 201, {
            'Location':location
        })
        
cdds_api = Blueprint('resources.cdds', __name__)
api = Api(cdds_api)
api.add_resource(
    CDD,
    '/api/v1/cdd/<int:id>',
    endpoint='cdd'
    )
api.add_resource(
    CDDs,
    '/api/v1/cdds',
    endpoint='cdds'
    )