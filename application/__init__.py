from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_jsglue import JSGlue
from flask_session import Session
from flask_admin import Admin
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
jwt = JWTManager(app)
jsglue = JSGlue(app)

#Session(app)
db = SQLAlchemy(app, session_options={"autoflush": True})

migrate = Migrate(app, db)

from application import views, models, forms, helpers
from application.resources.cdds import cdds_api
from application.resources.clients import clients_api
from application.resources.deliveries import deliveries_api
from application.resources.drivers import drivers_api
from application.resources.products import products_api
from application.resources.vehicles import vehicles_api

app.register_blueprint(cdds_api)
app.register_blueprint(clients_api)
app.register_blueprint(deliveries_api)
app.register_blueprint(drivers_api)
app.register_blueprint(products_api)
app.register_blueprint(vehicles_api)

