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

def bus_and_route():
  f = open("routes.csv")
  reader = csv.reader(f)
  new_bus = Bus(
    reg_no = random.randint(100000,999999),
    bus_identifier = "A",
    seats = 20,
    driver=1
  )
  db.session.add(new_bus)
  db.session.commit()
  for route_from,to in reader:
    new_route = Routes(
      route_from = route_from,
      route_to = to,
      depature_time = time(9, 00),
      bus = new_bus.id
    )
    db.session.add(new_route)
    db.session.commit()

def add_fleet_manager():
  fleet_manager = Fleet_Managers(
    username="Fleetmanager1",
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
    bus_and_route()
    # add_fleet_manager()
    # driver()
