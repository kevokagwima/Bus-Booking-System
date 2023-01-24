from flask import Flask, render_template, flash, url_for, redirect, request
from flask_login import login_manager, LoginManager, login_user, logout_user, login_required, current_user
from models import *
import random
from datetime import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_SILENCE_UBER_WARNING"] = 1
app.config["SECRET_KEY"] = 'judyonlinebookingproject'

login_manager = LoginManager()
login_manager.login_view = "/customer-login"
login_manager.login_message_category = "danger"
login_manager.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return Fleet_Managers.query.filter_by(phone_number=user_id).first() or Customers.query.filter_by(phone_number=user_id).first()
  except:
    flash(f"Failed to login the user", category="danger")

@app.route("/customer-registration", methods=["POST", "GET"])
def signup():
  if request.method == "POST":
    new_customer = Customers(
      customer_id = random.randint(100000,999999),
      fname = request.form.get("fname"),
      lname = request.form.get("lname"),
      phone_number = request.form.get("phone"),
      password = request.form.get("password"),
    )
    db.session.add(new_customer)
    db.session.commit()
    flash("Customer registered successfully", category="success")
    return redirect(url_for('signin'))

  return render_template("signup.html")

@app.route("/customer-login", methods=["POST", "GET"])
def signin():
  if request.method == "POST":
    customer = Customers.query.filter_by(phone_number=request.form.get("phone")).first()
    if customer:
      if customer.password == request.form.get("password"):
        login_user(customer, remember=True)
        flash("Login successfull", category="success")
        return redirect(url_for('index'))
      else:
        flash("Invalid login credentials", category="danger")
        return redirect(url_for('signin'))
    else:
      flash("No customer with that phone number", category="danger")
      return redirect(url_for('signin'))

  return render_template("signin.html")

@app.route("/fleetmanager-login", methods=["POST", "GET"])
def fleetmanager_signin():
  if request.method == "POST":
    fleetmanager = Fleet_Managers.query.filter_by(username=request.form.get("username")).first()
    if fleetmanager:
      if fleetmanager.password == request.form.get("password"):
        login_user(fleetmanager, remember=True)
        flash("Login successfull", category="success")
        return redirect(url_for('fleet_home'))
      else:
        flash("Invalid login credentials", category="danger")
        return redirect(url_for('fleetmanager_signin'))
    else:
      flash("No fleet manager with that username", category="danger")
      return redirect(url_for('fleetmanager_signin'))

  return render_template("fleetmanager_signin.html")

@app.route("/")
@app.route("/home")
def index():
  return render_template("index.html")

@app.route("/fleet-home")
@login_required
def fleet_home():
  buses = Bus.query.all()
  drivers = Drivers.query.all()
  routes = Routes.query.all()

  return render_template("fleet-home.html", buses=buses, drivers=drivers, routes=routes)

@app.route("/add-bus", methods=["POST", "GET"])
@login_required
def add_bus():
  bus_identifier = request.form.get("identifier").capitalize()
  all_bus_identifiers = []
  buses = Bus.query.all()
  for bus in buses:
    all_bus_identifiers.append(bus.bus_identifier)
  if bus_identifier in all_bus_identifiers:
    flash(f"Bus with identifier {bus_identifier} already exists", category="danger")
  else:
    new_bus = Bus(
      reg_no = random.randint(100000,999999),
      bus_identifier = request.form.get("identifier").capitalize(),
      seats = request.form.get("seats"),
      driver = request.form.get("driver")
    )
    db.session.add(new_bus)
    db.session.commit()
    flash("New bus added", category="success")
  return redirect(url_for('fleet_home'))

@app.route("/add-route", methods=["POST", "GET"])
@login_required
def add_route():
  new_route = Routes(
    route_from = request.form.get("from").capitalize(),
    route_to = request.form.get("to").capitalize(),
    price = request.form.get("price"),
    depature_time = time(9, 00),
    bus = request.form.get("bus")
  )
  db.session.add(new_route)
  db.session.commit()
  flash("New route added", category="success")
  return redirect(url_for('fleet_home'))

@app.route("/add-driver", methods=["POST", "GET"])
@login_required
def add_driver():
  new_driver = Drivers(
    username = request.form.get("username").capitalize(),
    password = "driver1",
  )
  db.session.add(new_driver)
  db.session.commit()
  flash("New driver added", category="success")
  return redirect(url_for('fleet_home'))

@app.route("/available-bus", methods=["POST", "GET"])
@login_required
def available_bus():
  if request.method == "POST":
    pickup = request.form.get("from").capitalize()
    destination = request.form.get("to").capitalize()
    available_buses = []
    routes = Routes.query.filter_by(route_from=pickup, route_to=destination).all()
    if routes:
      for route in routes:
        available_buses.append(route.bus)
      buses = Bus.query.all()
      if len(buses) == 1:
        flash(f"{len(available_buses)} bus found from {pickup} to {destination}", category="success")
      else:
        flash(f"{len(available_buses)} buses found from {pickup} to {destination}", category="success")
      return render_template("buses.html", routes=routes, available_buses=available_buses, buses=buses)
    else:
      flash(f"No buses found from {pickup} to {destination}", category="danger")
  else:
    flash("An error occured", category="danger")

  return redirect(url_for('index'))

@app.route("/select-bus/<int:bus_id>", methods=["POST", "GET"])
@login_required
def select_bus(bus_id):
  bus = Bus.query.get(bus_id)
  driver = Drivers.query.filter_by(id=bus.driver).first()
  route = Routes.query.filter_by(bus=bus.id).first()
  bookings = Booking.query.all()
  booked_seats = []
  if request.method == "POST":
    for booking in bookings:
      booked_seats.append(booking.seat)
    booked_seat = request.form.get("seats")
    if int(booked_seat) in booked_seats:
      flash("This seat has been already booked", category="danger")
      return redirect(url_for('select_bus', bus_id=bus.id))
    else:
      new_booking = Booking(
        customer = current_user.id,
        bus = bus.id,
        route = route.id,
        seat = booked_seat
      )
      db.session.add(new_booking)
      db.session.commit()
      flash("Your booking has been confirmed", category="success")
      return redirect(url_for('index'))

  return render_template("bus-details.html", bus=bus, driver=driver)

@app.route("/my-bookings")
@login_required
def my_bookings():
  bookings = Booking.query.filter_by(customer=current_user.id).all()
  buses = Bus.query.all()
  routes = Routes.query.all()
  driver = Drivers.query.all()

  return render_template("bookings.html", bookings=bookings, buses=buses, routes=routes, driver=driver)

@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Logout successfully", category="success")
  return redirect(url_for('signin'))

if __name__ == '__main__':
  app.run(debug=True)
