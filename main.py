from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_behind_proxy import FlaskBehindProxy
from services import *
from forms import RegistrationForm, LoginForm
import git
from dotenv import load_dotenv
import os
from models import db, User, Crystal

load_dotenv("/home/ukaylee/crystalarium/.env")

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db.init_app(app) # imported db from models!

with app.app_context():
    db.create_all()

@app.route("/")

def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/directory")
def directory():
  # crystals = load_crystals()
  crystals = Crystal.query.all()
  return render_template("directory.html", crystals=crystals)

@app.route("/saved")
def saves():
  user = get_current_user()

  if not user:
    return redirect(url_for("login"))

  crystals = user.user_saves
  return render_template("saved.html", crystals=crystals)

@app.route("/register", methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit(): # checks if entries are valid
    flash(f'Account created for {form.username.data}!', 'success')

    #new stuff from day 3
    user = User(username=form.username.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    session["user_id"] = user.id

    return redirect(url_for('home')) # if so - send to home page

  return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if request.method == "POST":
    user = User.query.filter_by(username=request.form["username"]).first()

    if user and user.password == request.form["password"]:
      session["user_id"] = user.id
      flash("Logged in successfully!", "success")
      return redirect(url_for("home"))

    flash("Invalid credentials", "danger")

  return render_template("login.html", form=form)

@app.route("/logout")
def logout():
  session.pop("user_id", None)
  return redirect(url_for("home"))

@app.route("/update_server", methods=['POST'])
def webhook():
  if request.method == 'POST':
    repo = git.Repo('/home/ukaylee/crystalarium')
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully', 200
  else:
    return 'Wrong event type', 400

@app.route("/save_crystal/<int:crystal_id>")
def save_crystal(crystal_id):
  user = get_current_user()

  if not user:
    return redirect(url_for("login"))

  crystal = Crystal.query.get(crystal_id)
  add_to_saves(user, crystal)
  return redirect(url_for("directory"))

@app.route("/unsave_crystal/<int:crystal_id>")
def unsave_crystal(crystal_id):
  user = get_current_user()

  if not user:
    return redirect(url_for("login"))

  crystal = Crystal.query.get(crystal_id)
  remove_from_saves(user, crystal)
  return redirect(url_for("saves"))

def get_current_user():
  user_id = session.get("user_id")
  if not user_id:
    return None
  user = User.query.get(user_id)
  return user 


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")