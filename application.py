from flask import Flask, render_template, flash, url_for, redirect, request
from flask_login import login_manager, LoginManager, login_user, logout_user, login_required
from models import *
import random

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'judyonlinebookingproject'

login_manager = LoginManager()
login_manager.login_view = "/customer-login"
login_manager.login_message_category = "danger"
login_manager.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return Customers.query.filter_by(phone_number=user_id).first()
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

@app.route("/")
@app.route("/home")
def index():
  return render_template("index.html")

@app.route("/available-bus", methods=["POST", "GET"])
def available_bus():
  if request.method == "POST":
    pickup = request.form.get("from").capitalize()
    destination = request.form.get("to").capitalize()
    buses = Bus.query.filter_by(route_from=pickup, route_to=destination).all()
    if buses:
      if len(buses) == 1:
        flash(f"{len(buses)} bus found", category="success")
      else:
        flash(f"{len(buses)} buses found", category="success")
      return render_template("buses.html", buses=buses)
    else:
      flash("No buses found", category="danger")
  else:
    flash("An error occured", category="danger")

  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(debug=True)
