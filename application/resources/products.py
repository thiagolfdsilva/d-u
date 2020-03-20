from flask import jsonify, Blueprint, url_for

from flask_restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with

from passlib.apps import custom_app_context as pwd_context

from application import models

from application import (
    db, JWTManager, jwt_required, create_access_token,
    get_jwt_identity, jwt
)

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'fit': fields.String
}

product_request_parser = reqparse.RequestParser()
product_request_parser.add_argument(
    'name',
    required=True,
    help='No name provided'
    )
product_request_parser.add_argument(
    'fit',
    required=True,
    help='No fit provided'
    )

class Product(Resource):
    def __init__(self):
        self.reqparse = product_request_parser
        super().__init__()
    
    @marshal_with(product_fields)
    def get(self, id):
        product = models.Product.query.filter_by(id=id).one()
        print(product.name)
        print(product.fit)
        return product
        
    @marshal_with(product_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Product.query.filter_by(id=id).update(**args)
        db.session.add(query)
        db.session.commit()
        return (models.Product.query.filter_by(id=id).one(), 200, {'Location' : url_for('resources.products.product', id=id)})
        
    def delete(self, id):
        query = models.Product.query.filter_by(id=id).one()
        db.session.delete(query)
        db.session.commit()
        return ('', 204, {'Location' : url_for('resources.products.products')})

class Products(Resource):
    def __init__(self):
        self.reqparse = product_request_parser
        super().__init__()
    
    def get(self):
        products = [marshal(product, product_fields) for
                    product in models.Product.query.all()]
        return {'products' : products}
        
    def post(self):
        args = self.reqparse.parse_args()
        product = models.Product(**args)
        db.session.add(product)
        db.session.commit()
        location = url_for('resources.products.product', id=product.id)
        return (product.id, 201, {
            'Location':location
        })
        
products_api = Blueprint('resources.products', __name__)
api = Api(products_api)
api.add_resource(
    Product,
    '/api/v1/product/<int:id>',
    endpoint='product'
    )
api.add_resource(
    Products,
    '/api/v1/products',
    endpoint='products'
    )