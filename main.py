from flask import Flask, render_template, url_for, flash, redirect, request
# from flask_behind_proxy import FlaskBehindProxy
from services import load_crystals
from forms import RegistrationForm
import git

# app = Flask(__name__)
# proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = "0d6a7916714408bffc2c5ceb0d976294" #need to put this in .env

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