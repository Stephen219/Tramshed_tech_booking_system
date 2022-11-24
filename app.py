from flask import Flask, render_template
from flask_migrate import Migrate
from flask_session import Session
from db import db

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


import user

if __name__ == "__main__":
    with app.app_context():
        # https://stackoverflow.com/a/45887721
        sess.app.session_interface.db.create_all()

    app.run(debug=True)
