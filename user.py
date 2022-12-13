from __main__ import app
from flask import (
    render_template,
    jsonify,
    request,
    session,
    redirect,
    url_for,
    session,
)
import functools
from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError
from db import Booking, Location, User, Review, Location
from datetime import datetime
import bcrypt
import random
import string

# https://stackoverflow.com/a/21456918
# Minimum eight characters, at least one letter, one number and one special character
PASSWORD_REGEX = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

# Schema validation from https://stackoverflow.com/a/61648076
class NewMemberSchema(Schema):
    first_name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="can't be empty"),
        error_messages={"required": "required"},
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(min=1, error="can't be empty"),
        error_messages={"required": "required"},
    )
    email = fields.Email(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    password = fields.String(
        required=True,
        validate=validate.Regexp(
            regex=PASSWORD_REGEX,
            error="password must contain a minimum of eight characters, at least one letter, one number and one special character",
        ),
        error_messages={"required": "required"},
    )

    class Meta:
        # Strip unknown values from output
        unknown = EXCLUDE


class UpdateMemberSchema(Schema):
    first_name = fields.String(
        validate=validate.Length(min=1, error="can't be empty"),
    )
    last_name = fields.String(
        validate=validate.Length(min=1, error="can't be empty"),
    )
    email = fields.Email(error_messages={"invalid": "invalid"})

    class Meta:
        # Strip unknown values from output
        unknown = EXCLUDE


class LoginSchema(Schema):
    email = fields.Email(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    password = fields.String(
        required=True,
        error_messages={"required": "required"},
    )

    class Meta:
        # Strip unknown values from output
        unknown = EXCLUDE


class ResetPasswordSchema(Schema):
    email = fields.Email(
        required=True, error_messages={"requires": "required", "invalid": "invalid"}
    )

    class Meta:
        unkown = EXCLUDE


class ChangePasswordSchema(Schema):
    email = fields.Email(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    password = fields.String(
        required=True,
        error_messages={"required": "required"},
    )
    token = fields.String(
        required=True,
        error_messages={"required": "required"},
    )

    class Meta:
        # Strip unknown values from output
        unknown = EXCLUDE


def ensure_login(func):
    @functools.wraps(func)
    def check_login(*args, **kwargs):
        logged_in = False
        sess_user_id = session.get("user_id")
        if not sess_user_id == None:
            logged_in = True
        if not logged_in and not "/auth/login" in request.path:
            return redirect(url_for("user_login"))
        if logged_in and "/auth/login" in request.path:
            return redirect(url_for("user_homepage"))
        db_user = User.get(sess_user_id)
        if db_user == None and logged_in:
            session.clear()
            return redirect("/")
        return func(db_user, *args, **kwargs)

    return check_login


@app.route("/account", methods=["GET", "PATCH", "DELETE"])
@ensure_login
def user_homepage(user):
    if request.method == "DELETE":
        User.delete(user["id"])

        session.clear()
        return redirect("/")
    if request.method == "PATCH":
        schema = UpdateMemberSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json
        User.update(user["id"], **body)

        return jsonify({"status": "success"})
    if request.method == "GET":
        db_locations = Location.getAll()
        db_locations.sort(key=lambda x: x["created_at"])
        db_locations = db_locations[:5]
        db_bookings = Booking.getAll()
        pending_bookings = Booking.getAll(status="PENDING")
        db_reviews = Review.getAll(user_id=user['id'])
        return render_template(
            "account/index.html", user=user, bookings=db_bookings, locations=db_locations, total_reviews=len(db_reviews), pending_bookings=len(pending_bookings), page="/"
        )


@app.get("/account/settings")
@ensure_login
def user_settings(user):
    return render_template("account/settings.html", user=user, page="/settings")


@app.get("/account/bookings")
@ensure_login
def user_bookings(user):
    sort_by = request.args.get("sort_by")
    db_bookings = Booking.getAll(user_id=user["id"])
    if sort_by == "atoz":
        db_bookings.sort(key=lambda x: x["location"]["name"])
    elif sort_by == "ztoa":
        db_bookings.sort(key=lambda x: x["location"]["name"], reverse=True)
    elif sort_by == "status":
        db_bookings.sort(key=lambda x: x["status"])
    elif sort_by == "from":
        db_bookings.sort(key=lambda x: x["location"]["created_at"])

    return render_template(
        "account/bookings.html",
        bookings=db_bookings,
        user=user,
    )


@app.route("/booking/<id>/cancel", methods=["POST", "GET"])
@ensure_login
def booking_deletion(user, id):
    db_booking = Booking.get(id)
    if db_booking == None:
        return "Not found", 404
    if request.method == "GET":
        return render_template("booking/cancel.html", user=user, booking=db_booking)
    if request.method == "POST":
        reason = request.form.get("reason")
        if reason == None:
            return "reason required", 400

        Booking.update(db_booking["id"], status="CANCELLED", cancellation_reason=reason)

        return "/account/bookings"


@app.route("/location/<id>/booking", methods=["POST", "GET"])
@ensure_login
def location_booking(user, id):
    db_location = Location.get(id)
    if db_location == None:
        return "Not found", 404
    if request.method == "GET":
        unreviewd_bookings = Booking.getAll(user_id=user["id"], location_id=id)
        all_bookings = Booking.getAll(location_id=id)
        return render_template(
            "location/booking.html",
            user=user,
            location=db_location,
            all_bookings=all_bookings,
            unreviewd_bookings=unreviewd_bookings,
            title="Book now",
        )
    if request.method == "POST":
        datein = request.form.get("datein")  # rem: args for get form for post
        dateout = request.form.get("dateout")
        comments = request.form.get("comments")
        indate = datetime.strptime(datein, "%Y-%m-%dT%H:%M")
        outdate = datetime.strptime(dateout, "%Y-%m-%dT%H:%M")
        data = Booking.new(
            checkin_date=indate,
            checkout_date=outdate,
            special_requests=comments,
            user_id=user["id"],
            location_id=db_location["id"],
        )
        return "/booking/" + data["id"] + "/confirmation"


@app.get("/bookings/review")
@ensure_login
def bookings_review(user):
    unreviewd_bookings = Booking.getAll(user_id=user["id"], review=None)

    return render_template(
        "location/review.html", user=user, unreviewd_bookings=unreviewd_bookings
    )


@app.post("/booking/<id>/review")
@ensure_login
def handle_review(user, id):
    db_booking = Booking.get(id)
    if db_booking == None:
        return "Not found", 404
    rating = request.form.get("rating")
    comment = request.form.get("comment")
    db_review = Review.new(
        rating=rating, comment=comment, user_id=user["id"], booking_id=db_booking["id"]
    )

    return "success"


@app.route("/booking/<id>/confirmation", methods=["POST", "GET"])
@ensure_login
def booking_confirmation(user, id):
    db_booking = Booking.get(id)
    if db_booking == None:
        return "Not found", 404
    return render_template("booking/confirmation.html", user=user, booking=db_booking)


@app.route("/auth/reset", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template("account/reset.html")
    if request.method == "POST":
        schema = ResetPasswordSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400
        body["email"] = body["email"].lower()
        db_user = User.query.filter_by(email=body["email"]).first()
        if db_user == None:
            return "success"
        temp_pass = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
        )
        # reset token could be encrypted for added security
        db_user.reset_token = temp_pass
        db.session.commit()
        print("/auth/change-password?" + "email=" + body["email"])
        print(temp_pass)
        return redirect("/auth/reset")


@app.route("/auth/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "GET":
        email = request.args.get("email").lower()
        if email == None:
            return "Not found", 404
        return render_template("/account/change.html")
    if request.method == "POST":
        schema = ChangePasswordSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400
        body["email"] = body["email"].lower()
        temp_pass = body["token"]
        db_user = User.query.filter_by(email=body["email"]).first()
        if temp_pass != db_user.reset_token:
            return "Invalid reset token", 401
        db_user.reset_token = None
        salt = bcrypt.gensalt()
        db_user.password = bcrypt.hashpw(str("password").encode("utf-8"), salt)
        db.session.commit()
        return redirect("/auth/login")


@app.get("/auth/logout")
def user_logout():
    # Clear session and redirect
    session.clear()
    return redirect("/")


@app.route("/auth/login", methods=["GET", "POST"])
@ensure_login
def user_login(user):
    if request.method == "GET":
        return render_template("account/login.html")
    if request.method == "POST":
        schema = LoginSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json
        db_user = User.getAll(email=body["email"])[0]

        if db_user == None or not bcrypt.checkpw(
            str(body["password"]).encode("utf-8"), db_user["password"]
        ):  # Check if user in db and also if password matches
            return ({"status": "error", "message": "Invalid credentials"}), 401
        session["user_id"] = db_user["id"]
        return jsonify({"status": "success"})


@app.route("/member/join", methods=["GET", "POST"])
def user_join():
    if request.method == "GET":
        return render_template("account/sign-up.html", PASSWORD_REGEX=PASSWORD_REGEX)
    if request.method == "POST":
        schema = NewMemberSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json
        body["email"] = body["email"].lower()
        db_user = User.getAll(email=body["email"])
        if len(db_user) > 1:  # Check if user in db already
            return jsonify({"email": ["already exists"]}), 400
        salt = bcrypt.gensalt()
        body["password"] = bcrypt.hashpw(str(body["password"]).encode("utf-8"), salt)
        body[
            "avatar"
        ] = "https://source.boringavatars.com/marble/120/{}%20{}?colors=FAD089,FF9C5B,F5634A,ED303C,3B8183".format(
            body["first_name"], body["last_name"]
        )
        data = User.new(**body)  # Turn input into db object

        session["user_id"] = data["id"]  # log user in after create account

        # TODO: Send account confirmation email

        return jsonify({"status": "success"})
