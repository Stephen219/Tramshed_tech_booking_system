from __main__ import app
from flask import render_template, jsonify, request, session, redirect, url_for
import functools
from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError
from user import PASSWORD_REGEX
from db import db, Admin, Location, Booking , User
import bcrypt

ALLOWED_EXTENXIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])
# Schema validation from https://stackoverflow.com/a/61648076


class CreateAccountSchema(Schema):
    username = fields.String(
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


class LoginSchema(Schema):
    username = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    password = fields.String(
        required=True,
        error_messages={"required": "required"},
    )

    class Meta:
        # Strip unknown values from output
        unknown = EXCLUDE


class CreateLocationSchema(Schema):
    name = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    address = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    main_photo = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    additional_photos = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    description = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    website = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    maps = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    email = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    phone_number = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    opening_hours = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )
    checkin_instructions = fields.String(
        required=True, error_messages={"required": "required", "invalid": "invalid"}
    )

    class Meta:
        # Strip unknown values from output
        unknown = EXCLUDE


def ensure_login(func):
    @functools.wraps(func)
    def check_login(*args, **kwargs):
        logged_in = False
        sess = session.get("admin_id")
        if not sess == None:
            logged_in = True
        if not logged_in and not "/_/auth/login" in request.path:
            return redirect(url_for("admin_login"))
        if logged_in and "/_/auth/login" in request.path:
            return redirect(url_for("admin_homepage"))
        db_admin = Admin.query.get(sess)
        if db_admin == None and logged_in:
            session.clear()
            return redirect("/_/")
        return func(db_admin, *args, **kwargs)

    return check_login


@app.get("/_/")
@ensure_login
def admin_homepage(admin):
    db_users=User.query.all()
    db_locations = Location.query.all()
    db_bookings = Booking.query.all()
    most_booked_index= 0
    most_booked_bookings = 0
    for location, i in enumerate(db_locations):
        # Check if the bookings in this location is more than most_booked_bookings
        # else continue

        return render_template("admin/index.html",total_users=len(db_users), total_locations=len(db_locations), total_bookings=len(db_bookings),admin=admin, page="/")


@app.get("/_/bookings")
@ensure_login
def admin_view_bookings(admin):
    db_bookings = Booking.query.all()
    return render_template(
        "admin/bookings table.html", admin=admin, page="/bookings", bookings=db_bookings
    )


@app.get("/_/settings")
@ensure_login
def admin_settings(admin):
    return render_template("admin/index.html", admin=admin, page="/settings")


@app.get("/_/locations")
@ensure_login
def admin_view_locations(admin):
    db_locations = Location.query.all()
    return render_template(
        "admin/locations.html", admin=admin, page="/locations", locations=db_locations
    )


@app.route("/_/locations/add", methods=["GET", "POST"])
@ensure_login
def add_locations(admin):
    if request.method == "GET":
        return render_template("admin/add/location.html")
    if request.method == "POST":
        schema = CreateLocationSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json

        data = Location(**body)  # Turn input into db object
        db.session.add(data)
        db.session.commit()
        return "/_/locations/" + data.id


@app.route("/_/locations/<id>", methods=["GET", "POST", "DELETE"])
@ensure_login
def confirm_details(admin, id):
    if request.method == "DELETE":
        db_location = Location.query.get(id)
        db.session.delete(db_location)
        db.session.commit()
        return "/_/locations"
    if request.method == "GET":
        db_location = Location.query.get(id)
        return render_template("admin/add/details.html", location=db_location)


@app.route("/_/bookings/manage", methods=["GET"])
@ensure_login
def manage_bookings(admin):
    if request.method == "GET":
        db_bookings = Booking.query.all()
        if not request.args.get('status') == None:
            db_bookings = Booking.query.filter_by(
                status=request.args.get('status'))
        return render_template("admin/bookings.html", bookings=db_bookings)


@app.route("/_/booking/<id>/approve", methods=["POST"])
@ensure_login
def approve_booking(admin, id):
    if request.method == "POST":
        db_bookings = Booking.query.get(id)
        db_bookings.status = "APPROVED"
        db.session.commit()
        return "/_/bookings/manage"


@app.route("/_/booking/<id>/decline", methods=["POST"])
@ensure_login
def decline_booking(admin, id):
    if request.method == "POST":
        db_bookings = Booking.query.get(id)
        db_bookings.status = "DECLINED"
        db.session.commit()
        return "/_/bookings/manage"


@app.get("/_/auth/logout")
def admin_logout():
    # Clear session and redirect
    session.clear()
    return redirect("/")


@app.route("/_/auth/login", methods=["GET", "POST"])
@ensure_login
def admin_login(admin):
    if request.method == "GET":
        db_admins = Admin.query.all()
        if len(db_admins) < 1:
            return redirect(url_for("admin_create"))
        return render_template("admin/login.html")
    if request.method == "POST":
        schema = LoginSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json
        db_admin = Admin.query.filter_by(username=body["username"]).first()
        if db_admin == None or not bcrypt.checkpw(
            str(body["password"]).encode("utf-8"), db_admin.password
        ):  # Check if user in db and also if password matches
            return ({"status": "error", "message": "Invalid credentials"}), 401
        session["admin_id"] = db_admin.id

        return jsonify({"status": "success"})


@app.route("/_/auth/create", methods=["GET", "POST"])
def admin_create():
    db_admins = Admin.query.all()
    if len(db_admins) > 0:
        return redirect("/_/auth/login")
    if request.method == "GET":
        return render_template("admin/create.html")
    if request.method == "POST":
        schema = CreateAccountSchema()
        try:
            body = schema.load(request.json)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Return errors in json

        salt = bcrypt.gensalt()
        body["password"] = bcrypt.hashpw(
            str(body["password"]).encode("utf-8"), salt)

        data = Admin(**body)  # Turn input into db object
        db.session.add(data)
        db.session.commit()

        session["admin_id"] = data.id  # log user in after create account
        return jsonify({"status": "success"})
