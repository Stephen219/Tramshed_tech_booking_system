from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import nanoid



db = SQLAlchemy()
# !Migration steps!
# Comment out any import(s) above if __name__ == "__main__": 
# To create a migration run -> flask db migrate -m "<message>"
# then to apply the migration to the db -> flask db upgrade
# Un-Comment the imports you commented


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    avatar = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

class Location(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    name= db.Column(db.String, nullable=False)
    address= db.Column(db.String, nullable=False)
    main_photo= db.Column(db.String, nullable=False)
    additional_photos= db.Column(db.String, nullable=False)
    description= db.Column(db.String, nullable=False)
    website= db.Column(db.String, nullable=False)
    maps= db.Column(db.String, nullable=False)
    email= db.Column(db.String, nullable=True)
    phone_number= db.Column(db.String, nullable=True)
    opening_hours= db.Column(db.String, nullable=False)
    checkin_instructions = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

class Booking(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    checkin_date = db.Column(db.DateTime(timezone=True), nullable=False)
    checkout_date = db.Column(db.DateTime(timezone=True), nullable=False)
    special_requests = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
