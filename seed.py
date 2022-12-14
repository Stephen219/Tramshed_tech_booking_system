import json
import sqlite3
from db import Location
import argparse


conn = sqlite3.connect("instance/data.db")

parser = argparse.ArgumentParser(
    description="""
    Adds the initial data to the db and also allows
    you to reset the db and update the schema
    """
)

parser.add_argument("-i", "--init", action="store_true")
args = parser.parse_args()

if args.init:
    with open("schema.sql") as f:
        conn.executescript(f.read())

cur = conn.cursor()


def seed_locations():
    with open("seed-data.json", "r", encoding="utf-8") as raw_data:
        data = json.load(raw_data)
        for location in data:
            cur.execute("SELECT * from location WHERE name=?", (location["name"],))
            db_location = cur.fetchall()
            if len(db_location) > 0:
                print("Skipping " + location["name"] + " as it already exists")
                continue
            print("Adding " + location["name"] + " to the db")
            del location['featured']
            Location.new(**location, featured=1)


if __name__ == "__main__":
    print("Starting seeding")
    print()
    seed_locations()
    print()
    print("Seeding completed")
    exit()
