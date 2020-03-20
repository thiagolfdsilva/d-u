import datetime

import json

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

chunk_fields = {
    'id': fields.Integer,
    'product': fields.Integer,
    'quanitty': fields.Integer,
    'delivery': fields.Integer
}

delivery_fields = {
    'id': fields.Integer,
    'cdd': fields.Integer,
    'client': fields.Integer,
    'chunks': fields.List(fields.Nested(chunk_fields))
}

booking_fields = {
    'id': fields.Integer,
    'driver': fields.Nested(driver_fields),
    'delivery': fields.Nested(delivery_fields),
    'status': fields.Integer,
    'created_at': fields.DateTime,
    'cancelling_time': fields.DateTime,
    'estimated_pickup_time': fields.DateTime,
    'estimated_delivery_time': fields.DateTime,
    'executed_pickup_time': fields.DateTime,
    'executed_delivery_time': fields.DateTime
}

class AddDelivery(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'cdd',
            required=True,
            help='No cdd provided'
            )
        self.reqparse.add_argument(
            'client',
            required=True,
            help='No client provided'
            )
        self.reqparse.add_argument(
            'chunk',
            action='append'
            )
        super().__init__()
        
    def post(self):
        args = self.reqparse.parse_args()
        delivery_data={}
        delivery_data['cdd_id']=args['cdd']
        delivery_data['client_id']=args['client']
        delivery_data['created_at']=datetime.datetime.now()
        newdelivery = models.Delivery(**delivery_data)
        db.session.add(newdelivery)
        db.session.flush()
        chunks=args['chunk']
        for c in chunks:
            chunk = json.loads(c)
            newchunk_data = {}
            newchunk_data['product_id']=chunk['product_id']
            newchunk_data['quantity']=chunk['quantity']
            newchunk_data['delivery_id']=newdelivery.id
            newchunk = models.Chunk(**newchunk_data)
            db.session.add(newchunk)
            db.session.flush()
        db.session.commit()
        location = url_for('resources.drivers.driver', id=newdelivery.id)
        return (newdelivery.id, 201, {
            'Location':location
        })
        
class GetBookings(Resource):
    def get(self, driver_id):
        bookings = [marshal(booking, booking_fields) for
                    booking in models.Booking.query.filter_by(driver=driver_id).all()]
        return {'bookings' : bookings}
        
class GetAllDeliveries(Resource):
    def get(self):
        deliveries_raw = models.Delivery.query.all()
        firstdelivery = models.Delivery.query.first()
        print(firstdelivery.id)
        deliveries = [marshal(delivery, delivery_fields) for
            delivery in deliveries_raw]
        return {"deliveries" : deliveries}
    
        
class AddBooking(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'delivery',
            required=True,
            help='No delivery provided',
            location=['form','json']
            )
        self.reqparse.add_argument(
            'estimated_pickup_time',
            required=True,
            help='No pickup time provided',
            location=['form','json']
            )
        super().__init__()
    
    @jwt_required    
    def post(self):
        args = self.reqparse.parse_args()
        new_booking_data=args.copy()
        new_booking_data['status']=1
        new_booking_data['created_at']=datetime.datetime.now
        new_booking_data['driver']=get_jwt_identity()
        new_booking = models.Booking(**new_booking_data)
        db.session.add(new_booking)
        db.session.commit()
        
class CancelBooking(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'booking',
            required=True,
            help='No booking provided',
            location=['form','json']
            )
        super().__init__()
        
    def post(self):
        args = reqparse.parse_args()
        booking = models.Booking.query.filter_by(id=args['booking']).one()
        booking.status=0
        db.session.add(booking)
        db.session.commit()
        
deliveries_api = Blueprint('resources.deliveries', __name__)
api = Api(deliveries_api)
api.add_resource(
    AddDelivery,
    '/api/v1/adddelivery',
    endpoint='add_delivery'
    )
api.add_resource(
    GetBookings,
    '/api/v1/getbookings/<int:driver_id>',
    endpoint='get_bookings'
    )
api.add_resource(
    AddBooking,
    '/api/v1/addbooking',
    endpoint='add_booking'
    )
api.add_resource(
    CancelBooking,
    '/api/v1/cancelbooking',
    endpoint='cancelbooking'
    )
api.add_resource(
    GetAllDeliveries,
    '/api/v1/getalldeliveries',
    endpoint='getalldeliveries'
    )