from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_session import Session
from db import db, Booking
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db.init_app(app)
# https://flask-migrate.readthedocs.io/en/latest/
Migrate(app, db)

app.config["SECRET_KEY"] = '<super secret key used for sessions>'
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 12  # Session valid for 12 hrs
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config["SESSION_SQLALCHEMY_TABLE"] = 'sessions'
app.config["SESSION_SQLALCHEMY"] = db

sess = Session(app)

@app.get("/")
def homepage():

    return render_template("index.html")

@app.route("/location/<id>/booking", methods = ['POST','GET'])
def location_booking(id):
    if request.method == "GET":
        return render_template("location/booking.html", id=id, title="Book now")
    if request.method == "POST":
        datein= request.form.get('datein')#rem: args for get form for post
        dateout = request.form.get('dateout')
        comments = request.form.get('comments')
        
        
        
        
        #datetime.strptime(dt_obj, format)
        
        
        indate =datetime.strptime(datein,'%Y-%m-%d')
        outdate =datetime.strptime(dateout,'%Y-%m-%d')
        
        
        data = Booking(checkin_date=indate, checkout_date=outdate, special_requests=comments)
        db.session.add(data)
        db.session.commit()
        
        return '/booking/'+ data.id + '/confirmation'
    

@app.route("/booking/<id>/confirmation", methods = ['POST','GET'])
def booking_confirmation(id):
    db_booking = Booking.query.get(id)
    if db_booking == None:
        return 'Not found', 404
    return render_template('booking/confirmation.html')

# /location/<id>/booking
# /booking/<id>/status - no_auth_required

import user

if __name__ == "__main__":
    with app.app_context():
        # https://stackoverflow.com/a/45887721
        sess.app.session_interface.db.create_all()

    app.run(debug=True)
