"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie,connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<user_id>")
def user_details(user_id):
    """Show user details"""

    user = User.query.filter(user_id==user_id).all()
    age = user.age
    zipcode = user.zipcode


    # user = db.relationship("User", backref=db.backref("ratings",order_by=rating_id))
    # movie = db.relationship("Movie",backref=db.backref("ratings",order_by=rating_id))

    return render_template("user_details.html", age=age, zipcode=zipcode)    

@app.route("/register", methods=["GET"])
def register_form():
    """Registering a user"""

    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    """Getting stored email and password"""

    email = request.form.get("email")
    password = request.form.get("password")
    
    query= User.query.filter(User.email == email).first()

    if not query:
        user = User(email=email,password=password)
        db.session.add(user)
        db.session.commit()


    return redirect("/")

@app.route("/login")
def login_info():

    return render_template("login_form.html")

@app.route("/logged_in", methods=['GET','POST'])
def logged_in():

    email = request.form.get("email")
    password = request.form.get("password")

    #Email and password query check if mateches
    query = User.query.filter(User.email == email , User.password == password).first()


    if query:
        session['user_id'] = query.user_id
        flash('You are successfully logged in')
        return redirect('/')

    else:
        return redirect('/login')

@app.route("/logged_out")
def logged_out():

    session.pop('user_id', None)
    flash("You are logged out")

    return redirect('/')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
