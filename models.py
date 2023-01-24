from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Customers(db.Model, UserMixin):
  __tablename__ = 'customers'
  id = db.Column(db.Integer(), primary_key=True)
  customer_id = db.Column(db.Integer(), unique=True, nullable=False)
  fname = db.Column(db.String(20), nullable=False)
  lname = db.Column(db.String(20), nullable=False)
  phone_number = db.Column(db.String(10), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  booking = db.relationship("Booking", backref="booking-customer", lazy=True)

class Fleet_Managers(db.Model, UserMixin):
  __tablename__ = 'fleet-managers'
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(30), nullable=False, unique=True)
  phone_number = db.Column(db.String(10), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)

class Drivers(db.Model):
  __tablename__ = 'drivers'
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(30), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  bus = db.relationship("Bus", backref="my-bus", lazy=True)

class Bus(db.Model):
  __tablename__ = 'bus'
  id = db.Column(db.Integer(), primary_key=True)
  reg_no = db.Column(db.Integer(), nullable=False, unique=True)
  bus_identifier = db.Column(db.String(1), nullable=False, unique=True)
  seats = db.Column(db.Integer(), nullable=False)
  driver = db.Column(db.Integer(), db.ForeignKey("drivers.id"))
  route = db.relationship("Routes", backref="bus-route", lazy=True)
  booking = db.relationship("Booking", backref="booking-bus", lazy=True)

class Routes(db.Model):
  __tablename__ = 'routes'
  id = db.Column(db.Integer(), primary_key=True)
  route_from = db.Column(db.String(20), nullable=False)
  route_to = db.Column(db.String(20), nullable=False)
  depature_time = db.Column(db.Time(), nullable=False)
  price = db.Column(db.Integer(), nullable=False)
  bus = db.Column(db.Integer(), db.ForeignKey("bus.id"))
  booking = db.relationship("Booking", backref="booking-route", lazy=True)

class Booking(db.Model):
  __tablename__ = 'bookings'
  id = db.Column(db.Integer(), primary_key=True)
  customer = db.Column(db.Integer(), db.ForeignKey("customers.id"))
  bus = db.Column(db.Integer(), db.ForeignKey("bus.id"))
  route = db.Column(db.Integer(), db.ForeignKey("routes.id"))
  seat = db.Column(db.Integer(), unique=True, nullable=False)
