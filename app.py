import functools
from flask import Flask, render_template, session
from flask_migrate import Migrate
from flask_session import Session
from db import db, User

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
    locations = [
        {
            "id": "test-id",
            "name": "Stafion F",
            "opening_hours": "6am - 10pm",
            "total_spaces": 12,
            "rating": 1.1,
            "main_photo": "https://stationf.co/img/misc/create-zone.jpg"
        },
        {
            "id": "test-id-2",
            "name": "Dogpatch Labs",
            "opening_hours": "6am - 6pm",
            "total_spaces": 12,
            "rating": 3.4,
            "main_photo": "https://dogpatchlabs.wpenginepowered.com/wp-content/uploads/2022/09/ian_browne.jpg"
        },
    ]
    return render_template("index.html", user=user, locations=locations)


import user

if __name__ == "__main__":
    with app.app_context():
        # https://stackoverflow.com/a/45887721
        sess.app.session_interface.db.create_all()

    app.run(debug=True)
