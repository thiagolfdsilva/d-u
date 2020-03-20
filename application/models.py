from application import db

#class Authentication(db.Model):
#    __tablename__ = 'authentication'
#    id = db.Column(db.Integer, primary_key=True)
#    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#    passwordhsh = db.Column(db.String)
#    def __repr__(self):
#        return '%r' % (self.user_id)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    cancelling_time = db.Column(db.DateTime)
    estimated_pickup_time = db.Column(db.DateTime)
    estimated_delivery_time = db.Column(db.DateTime)
    executed_pickup_time = db.Column(db.DateTime)
    executed_delivery_time = db.Column(db.DateTime)
        
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    deliveries = db.relationship('Delivery', backref='client', lazy='dynamic')
        
class CDD(db.Model):
    __tablename__ = 'cdds'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    deliveries = db.relationship('Delivery', backref='cdd', lazy='dynamic')
    
#A chunk is a grouping of similar products in a given delivery
#A delivery is made of many chunks
class Chunk(db.Model):
    __tablename__ = 'chunks'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_id = db.Column(db.Integer, db.ForeignKey('deliveries.id'), nullable=False)
    
class Delivery(db.Model):
    __tablename__ = 'deliveries'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    cdd_id = db.Column(db.Integer, db.ForeignKey("cdds.id"), nullable=False)
    price = db.Column(db.Numeric(8,2))
    final_date = db.Column(db.DateTime)
    chunks = db.relationship('Chunk', backref="delivery", lazy='dynamic')
    bookings = db.relationship('Booking', backref="delivery", lazy='dynamic')
    #timeslots?

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String)
    bookings = db.relationship('Booking', backref="driver", lazy='dynamic')
    auth = db.relationship('DriverAuth', backref='driver', uselist=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)

    
class DriverAuth(db.Model):
    __tablename__ = 'driverauth'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=False)
    password_hash = db.Column(db.String)
    def __repr__(self):
        return '%r' % (self.id)    
    
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fit = db.Column(db.Integer) #size-related, how many of those "fit" in a standard measure
    chunks = db.relationship('Chunk', backref='product', lazy='dynamic')
    def __repr__(self):
        return '%r' % (self.name)
    
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    capacity = db.Column(db.Integer)
    icon = db.Column(db.String)
    drivers = db.relationship('Driver', backref="vehicle", lazy='dynamic')
