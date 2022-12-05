from __main__ import app
from flask import render_template, jsonify, request, session, redirect, url_for
import functools
from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError
from db import db, User , Booking, Location
from datetime import datetime
import bcrypt

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


def ensure_login(func):
    @functools.wraps(func)
    def check_login(*args, **kwargs):
        logged_in = False
        sess = session.get("user_id")
        if not sess == None:
            logged_in = True
        if not logged_in and not "/auth/login" in request.path:
            return redirect(url_for("user_login"))
        if logged_in and "/auth/login" in request.path:
            return redirect(url_for("user_homepage"))
        db_user = User.query.get(sess)
        if db_user == None and logged_in:
            session.clear()
            return redirect("/")
        return func(db_user, *args, **kwargs)

    return check_login


@app.route("/account", methods=["GET", "PATCH", "DELETE"])
@ensure_login
def user_homepage(user):
    if request.method == "DELETE":
        db_user = User.query.get(user.id)
        db.session.delete(db_user)
        db.session.commit()

        session.clear()
        return redirect("/")
    if request.method == "PATCH":
        schema = UpdateMemberSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json
        db_user = User.query.get(user.id)
        db_user.first_name = body["first_name"]
        db_user.last_name = body["last_name"]
        db_user.email = body["email"]
        db.session.commit()

        return jsonify({"status": "success"})
    db_bookings = Booking.query.filter_by(user=user).all()
    return render_template("account/index.html", user=user, bookings=db_bookings, page="/")

@app.get("/account/settings")
@ensure_login
def user_settings(user):
    return render_template("account/settings.html", user=user, page="/settings")


@app.get("/account/bookings")
@ensure_login
def user_bookings(user):
    db_bookings = Booking.query.filter_by(user=user).all()
    bookings = [{"location": {"id":"test","name": "station f"},
                 "checkin_date": datetime.now(), "checkout_date": datetime.now(),
                 "created_at": datetime.now(),
                 "status": "PENDING"
                 }]
    return render_template("account/bookings.html", bookings=db_bookings, user=user,)

@app.route("/booking/<id>/cancel", methods = ['POST','GET','PATCH','DELETE'])
@ensure_login
def booking_deletion(user,id): 
    db_booking=Booking.query.get(id)
    if db_booking == None:
        return "Not found", 404
    if request.method== "GET":
        print(id)
        return render_template('account/delete.html',user=user, booking=db_booking )
   
    if request.method== "POST":
        db_booking.status = "CANCELLED"
        db.session.commit()
        print("success")
        return "/account/bookings"

    
            
        
        








@app.route("/location/<id>/booking", methods=['POST', 'GET'])
@ensure_login
def location_booking(user,id):
    db_location = Location.query.get(id)
    if db_location == None:
        return "Not found", 404
    if request.method == "GET":
        return render_template("location/booking.html", user=user, location=db_location, title="Book now")
    if request.method == "POST":
        datein = request.form.get('datein')  # rem: args for get form for post
        dateout = request.form.get('dateout')
        comments = request.form.get('comments')
        indate =datetime.strptime(datein,'%Y-%m-%dT%H:%M')
        outdate =datetime.strptime(dateout,'%Y-%m-%dT%H:%M')
        data = Booking(checkin_date=indate, checkout_date=outdate, special_requests=comments,user=user, location=db_location)
        db.session.add(data)
        db.session.commit()
        return '/booking/' + data.id + '/confirmation'


    
@app.route("/booking/<id>/confirmation", methods = ['POST','GET'])
@ensure_login
def booking_confirmation(user,id):
    db_booking = Booking.query.get(id)
    if db_booking == None:
        return 'Not found', 404
    return render_template('booking/confirmation.html', user=user, booking=db_booking)
@app.get("/My-bookings")
@ensure_login
def My_bookings(user):
    db_bookings = Booking.query.filter_by(user_id=user.id).all()
    print(db_bookings)
    return "db_bookings"


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
        db_user = User.query.filter_by(email=body["email"]).first()

        if db_user == None or not bcrypt.checkpw(
            str(body["password"]).encode("utf-8"), db_user.password
        ):  # Check if user in db and also if password matches
            return ({"status": "error", "message": "Invalid credentials"}), 401
        session["user_id"] = db_user.id
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
        db_user = User.query.filter_by(email=body["email"]).first()
        if not db_user == None:  # Check if user in db already
            return jsonify({"email": ["already exists"]}), 400
        salt = bcrypt.gensalt()
        body["password"] = bcrypt.hashpw(
            str(body["password"]).encode("utf-8"), salt)
        body[
            "avatar"
        ] = "https://source.boringavatars.com/marble/120/{}%20{}?colors=FAD089,FF9C5B,F5634A,ED303C,3B8183".format(
            body["first_name"], body["last_name"]
        )
        data = User(**body)  # Turn input into db object
        db.session.add(data)
        db.session.commit()

        session["user_id"] = data.id  # log user in after create account

        # TODO: Send account confirmation email

        return jsonify({"status": "success"})
