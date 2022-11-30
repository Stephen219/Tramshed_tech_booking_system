import functools
from flask import Flask, request,render_template, session
from flask_migrate import Migrate
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from db import db, User, Location, Booking
from datetime import datetime
ALLOWED_EXTENXIONS= set(['txt','pdf','png','jpg','jpeg','gif'])

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# https://stackoverflow.com/questions/9692962/flask-sqlalchemy-import-context-issue/9695045#9695045
db.init_app(app)
# https://flask-migrate.readthedocs.io/en/latest/
Migrate(app, db)

app.config["SECRET_KEY"] = "<super secret key used for sessions>"
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 12  # Session valid for 12 hrs
# TODO: Work on clearing session from db
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY_TABLE"] = "sessions"
app.config["SESSION_SQLALCHEMY"] = db
sess = Session(app)


def use_user(func):
    @functools.wraps(func)
    def get_user(*args, **kwargs):
        sess_user_id = session.get("user_id")
        if sess_user_id == None:
            return func(None, *args, **kwargs)
        db_user = User.query.get(sess_user_id)
        if not db_user == None:
            return func(db_user, *args, **kwargs)

        return func(None, *args, **kwargs)

    return get_user


@app.get("/")
@use_user
def homepage(user):
    return render_template("index.html", user=user)

@app.get("/locations")
def location_page():
    db_locations = Location.query.all()
    return render_template("locations.html", data=db_locations)

@app.get("/location/add")
def location_temp_add():
    data =Location(
    name="Codebase",
    address="CodeBase Edinburgh , 37a Castle Terrace, Edinburgh, EH1 2EL",
    main_photo="https://images.squarespace-cdn.com/content/v1/55439320e4b0f92b5d6c4c8b/1646867535415-4JI39H286BUMT26H4FHN/C36A1915.jpg?format=2500w",
    additional_photos="https://images.squarespace-cdn.com/content/v1/55439320e4b0f92b5d6c4c8b/1646868533510-J1OT4PEG5VM9FCBF8BJE/15.10.19_-_CREATIVE_BRIDGE_C02_-_DAY01_-_LQ-19+%281%29.jpg?format=2500w,https://images.squarespace-cdn.com/content/v1/55439320e4b0f92b5d6c4c8b/1646868421127-07KQ4N1OHTDDKQME686A/15.10.19_-_CREATIVE_BRIDGE_C02_-_DAY01_-_LQ-52+%281%29.jpg?format=2500w",
    description="Hi. We\u2019re CodeBase. We've been exploring the world of startups and innovation for over five years now. We're not really sure how to best describe what we do, but we think the words \"tech cluster\" probably do it best. Please get in touch! We\u2019re friendly people who are geeky about building tech startups, managing disruption and innovation.",
    website="https://www.thisiscodebase.com",
    maps="https://www.bing.com/maps?osid=bdd66ada-e1f7-4a12-84e0-36cabf916339&cp=55.946977~-3.20657&lvl=16&pi=0&imgid=2541f778-2244-4aac-bd44-0cd70405213f&v=2&sV=2&form=S00027",
    email="info@thisiscodebase.com",
    phone_number="(+44) 0131 560 2003",
    opening_hours="08:00 - 17:00",
    checkin_instructions="Use the email address or phone number to call ahead and book a desk, let them know you're a Tramshed member",
    )
    db.session.add(data)
    db.session.commit()
    return "succes"

@app.route("/location/<id>/booking", methods = ['POST','GET'])
def location_booking(id):
    if request.method == "GET":
        return render_template("location/booking.html", id=id, title="Book now")
    if request.method == "POST":
        datein= request.form.get('datein')#rem: args for get form for post
        dateout = request.form.get('dateout')
        comments = request.form.get('comments')
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
@app.get("/My bookings/")
def My_bookings(id):
    db_bookings = Booking.query.filter_by(user_id=["user_id"]).first()
    return render_template


import user

if __name__ == "__main__":
    with app.app_context():
        # https://stackoverflow.com/a/45887721
        sess.app.session_interface.db.create_all()

    app.run(debug=True)
