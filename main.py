from flask import Flask, render_template, url_for, flash, redirect, request
# from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from services import load_crystals
from forms import RegistrationForm
import git

app = Flask(__name__)
# proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = "0d6a7916714408bffc2c5ceb0d976294" #need to put this in .env

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

with app.app_context():
  db.create_all()

@app.route("/")

def home():
    return render_template('index.html')
    
@app.route("/gallery")
def gallery():
    return render_template('gallery.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/tracker")
def tracker():
    return render_template('tracker.html')

@app.route("/directory")
def directory():
    crystals = load_crystals()
    return render_template("directory.html", crystals=crystals)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page

        #new stuff from day 3
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)

# @app.route("/update_server", methods=['POST'])
# def webhook():
#     if request.method == 'POST':
#         repo = git.Repo('/home/ukaylee/crystalarium')
#         origin = repo.remotes.origin
#         origin.pull()
#         return 'Updated PythonAnywhere successfully', 200
#     else:
#         return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")