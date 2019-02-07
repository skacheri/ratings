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

@app.route("/logged_in", methods=["POST"])
def logged_in():
    email = request.form.get("email")
    password = request.form.get("password")
    print("\n\n\n\n\n\n")
    print(email)
    print(password)

    
    #Email and password query check if mateches
    query = User.query.filter(User.email == email , User.password == password).first()

    print("\n\n\n\n\n\n")
    print(query)
    

    if query:
        session['user_id'] = query.user_id
        return redirect('/')
    else:
        return redirect('/login')




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
