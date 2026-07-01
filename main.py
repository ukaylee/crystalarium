from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from services import *
from forms import RegistrationForm
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
    # crystals = load_crystals()
    user = User.query.get(1)
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
        return redirect(url_for('home')) # if so - send to home page

    return render_template('register.html', form=form)

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
    user = User.query.get(1)
    crystal = Crystal.query.get(crystal_id)
    add_to_saves(user, crystal)
    return redirect(url_for("directory"))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")