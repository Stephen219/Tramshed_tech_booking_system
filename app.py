import functools
from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from random import choice
from db import DATABASE, User, Location, Booking

ALLOWED_EXTENXIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

app = Flask(__name__)

app.config["SECRET_KEY"] = "<super secret key used for sessions>"
app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 12  # Session valid for 12 hrs
# TODO: Work on clearing session from db
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "instance/sess"

sess = Session(app)


def use_user(func):
    @functools.wraps(func)
    def get_user(*args, **kwargs):
        sess_user_id = session.get("user_id")
        if sess_user_id == None:
            return func(None, *args, **kwargs)
        db_user = User.get(sess_user_id)
        if not db_user == None:
            return func(db_user, *args, **kwargs)

        return func(None, *args, **kwargs)

    return get_user


@app.get("/")
@use_user
def homepage(user):
    db_locations = Location.getAll()
    edited_locations = []
    for location in db_locations:
        location = dict(location)
        db_all_bookings = Booking.getAll(location_id=location["id"])
        db_bookings = [i for i in db_all_bookings if not (i["review"] == None)]
        location["avg_rating"] = 0
        if len(db_bookings) > 0:
            location["randomReview"] = choice(db_bookings)["review"]
            location["avg_rating"] = sum(
                booking["review"]["rating"] for booking in db_bookings
            ) / len(db_bookings)
        edited_locations.append(location)

    # FIXME: Reviews and ratings need to be displayed
    return render_template("index.html", user=user, locations=edited_locations)


@app.get("/locations")
@use_user
def location_page(user):
    db_locations = Location.getAll()
    return render_template("locations.html", user=user, data=db_locations)


import user
import admin

if __name__ == "__main__":
    app.run(debug=True)
