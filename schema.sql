DROP TABLE IF EXISTS admin;
DROP TRIGGER IF EXISTS adminUpdatedAt;
DROP TABLE IF EXISTS user;
DROP TRIGGER IF EXISTS userUpdatedAt;
DROP TABLE IF EXISTS location;
DROP TRIGGER IF EXISTS bookingUpdatedAt;
DROP TABLE IF EXISTS booking;
DROP TRIGGER IF EXISTS bookingUpdatedAt;
DROP TABLE IF EXISTS review;
DROP TRIGGER IF EXISTS reviewUpdatedAt;

CREATE TABLE admin (
  id TEXT PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TRIGGER adminUpdatedAt AFTER UPDATE ON admin
BEGIN
  update admin SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TABLE user (
  id TEXT PRIMARY KEY,
  avatar  TEXT NOT NULL,
  email  TEXT NOT NULL,
  first_name  TEXT NOT NULL,
  last_name  TEXT NOT NULL,
  password  TEXT NOT NULL,
  reset_token TEXT,
  -- bookings relationship
  -- reviews relationship
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TRIGGER userUpdatedAt AFTER UPDATE ON user
BEGIN
  update user SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TABLE location (
  id TEXT PRIMARY KEY,
  name  TEXT NOT NULL,
  status  TEXT NOT NULL,
  address  TEXT NOT NULL,
  main_photo  TEXT NOT NULL,
  additional_photos  TEXT NOT NULL,
  description  TEXT NOT NULL,
  website  TEXT NOT NULL,
  maps  TEXT NOT NULL,
  email  TEXT,
  phone_number  TEXT,
  checkin_instructions  TEXT NOT NULL,
  -- bookings relationship
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TRIGGER locationUpdatedAt AFTER UPDATE ON location
BEGIN
  update booking SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TABLE booking (
  id TEXT PRIMARY KEY,
  status  TEXT NOT NULL,
  special_requests TEXT,
  cancellation_reason TEXT,
  checkin_date TIMESTAMP NOT NULL,
  checkout_date TIMESTAMP NOT NULL,
  location_id REFERENCES  location(id),
  user_id REFERENCES  user(id),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TRIGGER bookingUpdatedAt AFTER UPDATE ON booking
BEGIN
  update booking SET updated_at = datetime('now') WHERE id = NEW.id;
END;

CREATE TABLE review (
  id TEXT PRIMARY KEY,
  rating INTEGER NOT NULL,
  comment TEXT,
  booking_id REFERENCES  booking(id),
  user_id REFERENCES  user(id),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TRIGGER reviewUpdatedAt AFTER UPDATE ON review
BEGIN
  update review SET updated_at = datetime('now') WHERE id = NEW.id;
END;