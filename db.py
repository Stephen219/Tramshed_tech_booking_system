from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.sql import func
import nanoid

# Fix for valueerror: https://stackoverflow.com/a/62651160
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
# !Migration steps!
# Check README.md on gitlab

class Admin(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    avatar = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    bookings= db.relationship('Booking', backref = 'user')
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
    bookings= db.relationship('Booking', backref='location')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    

class Booking(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    status = db.Column(db.String, default="PENDING")
    checkin_date = db.Column(db.DateTime(timezone=True), nullable=False)
    checkout_date = db.Column(db.DateTime(timezone=True), nullable=False)
    special_requests = db.Column(db.String, nullable=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    location_id = db.Column(db.String, db.ForeignKey('location.id'))
    location_name= db.Column(db.String, db.ForeignKey('location.name'))
    review_id = db.Column(db.String, db.ForeignKey('review.id'))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
class Review(db.Model):
    id = db.Column(db.String, primary_key=True, default=nanoid.generate)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=True)
    location_id=db.Column(db.String, nullable=False)
    booking_id=db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())