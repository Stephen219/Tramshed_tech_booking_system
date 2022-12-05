from flask import Flask, render_template, session
from db import db,Location
import json

app = Flask('seed-db')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def seed_locations():
    with open("seed-data.json", "r", encoding='utf-8') as raw_data:
        data = json.load(raw_data)
        for location in data:
            db_location = Location.query.filter_by(name=location["name"]).all()
            if len(db_location) > 0:
                print("Skipping "+location["name"]+ " as it already exists")
                continue
            print("Adding "+location["name"]+ " to the db")
            db_location = Location(**location)
            db.session.add(db_location)
            db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        print("Starting seeding")
        print()
        seed_locations()
        print()
        print("Seeding completed")
        exit()