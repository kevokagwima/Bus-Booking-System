from flask import Flask
from models import *
import csv, random
from datetime import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def main():
  db.create_all()

def bus():
  bus = open("bus.csv")
  routes = open("routes.csv")
  reader = csv.reader(bus)
  readers = csv.reader(routes)
  for identifier,seats,driver in reader:
    new_bus = Bus(
      reg_no = random.randint(100000,999999),
      bus_identifier = identifier,
      seats = seats,
      driver = driver
    )
    db.session.add(new_bus)
    db.session.commit()
    for route_from,to,price in readers:
      new_route = Routes(
        route_from = route_from,
        route_to = to,
        depature_time = time(9, 00),
        bus = new_bus.id,
        price = price
      )
      db.session.add(new_route)
      db.session.commit()

def add_fleet_manager():
  fleet_manager = Fleet_Managers(
    username="Fleetmanager1",
    phone_number="0758632102",
    password="fleet1",
  )
  db.session.add(fleet_manager)
  db.session.commit()
  print("Fleet manager addedd")

def driver():
  driver = Drivers(
    username="Driver1",
    password="fleet1",
  )
  db.session.add(driver)
  db.session.commit()
  print("Driver manager addedd")

if __name__ == '__main__':
  with app.app_context():
    # main()
    # bus()
    add_fleet_manager()
    # driver()
