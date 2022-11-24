from __main__ import app
from flask import render_template, jsonify, request, session, redirect, url_for
import functools
from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError
from db import db, User
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
        if not session.get('user_id') == None:
            logged_in = True
        if not logged_in and not '/auth/login' in request.path:
            return redirect(url_for("user_login"))
        if logged_in and '/auth/login' in request.path:
            return redirect(url_for('user_homepage'))

        return func(*args, **kwargs)

    return check_login

@app.get("/account")
@ensure_login
def user_homepage():
    return render_template('account/index.html')

@app.get("/auth/logout")
def user_logout():
    # Clear session and redirect
    session.clear()
    return redirect("/")


@app.route("/auth/login", methods=["GET", "POST"])
@ensure_login
def user_login():
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
        body["password"] = bcrypt.hashpw(str(body["password"]).encode("utf-8"), salt)
        body[
            "avatar"
        ] = "https://source.boringavatars.com/marble/120/{}%20{}?colors=FAD089,FF9C5B,F5634A,ED303C,3B8183".format(
            body["first_name"], body["last_name"]
        )
        data = User(**body)  # Turn input into db object
        db.session.add(data)
        db.session.commit()

        session["user_id"] = data.id # log user in after create account

        # TODO: Send account confirmation email

        return jsonify({"status": "success"})
