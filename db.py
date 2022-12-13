from itertools import groupby
import sqlite3
import nanoid

DATABASE = "instance/data.db"


def get_db():
    conn = sqlite3.connect(
        DATABASE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return [conn, cur]


class Admin:
    def new(**data) -> dict:
        parsed_data = {
            "id": nanoid.generate(),
            "username": data["username"],
            "password": data["password"],
        }
        [conn, cur] = get_db()
        cols = ", ".join(parsed_data.keys())
        placeholders = ":" + ", :".join(parsed_data.keys())
        sql = "INSERT INTO admin (%s) VALUES (%s)" % (cols, placeholders)
        cur.execute(sql, parsed_data)
        conn.commit()
        conn.close()

        return parsed_data

    def get(id: str) -> None | dict:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE id=?", (id,))
        db_user = cur.fetchone()
        conn.close()

        return db_user

    def getAll(**query) -> None | list:
        qs = []
        for key, _ in query.items():
            qs.append("{}=?".format(key))
        [conn, cur] = get_db()
        sql = "SELECT * FROM admin"
        if len(query.keys()) >= 1:
            # It errors when you dont provide anything
            sql = "SELECT * FROM admin WHERE {}".format(" AND ".join(qs))
        cur.execute(sql, (*query.values(),))
        db_locations = cur.fetchall()
        conn.close()

        return db_locations

    def update(id, **data) -> dict:
        [conn, cur] = get_db()
        cols = ", ".join(k + "=?" for k in data.keys())
        sql = "UPDATE admin SET %s WHERE id=?" % (cols)
        cur.execute(
            sql,
            (
                *data.values(),
                id,
            ),
        )
        conn.commit()
        conn.close()

        return User.get(id)

    def delete(id: str):
        [conn, cur] = get_db()
        sql = "DELETE FROM admin WHERE id=?"
        cur.execute(sql, (id,))
        conn.commit()
        conn.close()


class User:
    def new(**data) -> dict:
        parsed_data = {
            "id": nanoid.generate(),
            "avatar": data["avatar"],
            "email": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "password": data["password"],
        }
        [conn, cur] = get_db()
        cols = ", ".join(parsed_data.keys())
        placeholders = ":" + ", :".join(parsed_data.keys())
        sql = "INSERT INTO user (%s) VALUES (%s)" % (cols, placeholders)
        cur.execute(sql, parsed_data)
        conn.commit()
        conn.close()

        return parsed_data

    def get(id: str) -> None | dict:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE id=?", (id,))
        db_user = cur.fetchone()
        conn.close()

        return db_user

    def getAll(**query) -> None | list:
        qs = []
        for key, _ in query.items():
            qs.append("{}=?".format(key))
        [conn, cur] = get_db()
        sql = "SELECT * FROM user"
        if len(query.keys()) >= 1:
            # It errors when you dont provide anything
            sql = "SELECT * FROM user WHERE {}".format(" AND ".join(qs))
        cur.execute(sql, (*query.values(),))
        db_locations = cur.fetchall()
        conn.close()

        return db_locations

    def update(id, **data) -> dict:
        [conn, cur] = get_db()
        cols = ", ".join(k + "=?" for k in data.keys())
        sql = "UPDATE user SET %s WHERE id=?" % (cols)
        cur.execute(
            sql,
            (
                *data.values(),
                id,
            ),
        )
        conn.commit()
        conn.close()

        return User.get(id)

    def delete(id: str):
        [conn, cur] = get_db()
        sql = "DELETE FROM user WHERE id=?"
        cur.execute(sql, (id,))
        conn.commit()
        conn.close()


class Location:
    def new(**data) -> dict:
        parsed_data = {
            "id": nanoid.generate(),
            "name": data["name"],
            "status": "AVAILABLE",
            "featured": data["featured"],
            "address": data["address"],
            "main_photo": data["main_photo"],
            "additional_photos": data["additional_photos"],
            "description": data["description"],
            "website": data["website"],
            "maps": data["maps"],
            "email": data["email"],
            "phone_number": data["phone_number"],
            "checkin_instructions": data["checkin_instructions"],
            "features": data["features"],
        }
        [conn, cur] = get_db()
        cols = ", ".join(parsed_data.keys())
        placeholders = ":" + ", :".join(parsed_data.keys())
        sql = "INSERT INTO location (%s) VALUES (%s)" % (cols, placeholders)
        cur.execute(sql, parsed_data)
        conn.commit()
        conn.close()

        return parsed_data

    def get(id: str) -> None | dict:
        [conn, cur] = get_db()
        cur.execute("SELECT * FROM location WHERE id=?", (id,))
        db_location = cur.fetchone()

        conn.close()

        return db_location

    def getAll(**query) -> None | list:
        qs = []
        for key, _ in query.items():
            qs.append("{}=?".format(key))
        [conn, cur] = get_db()
        sql = "SELECT * FROM location"
        if len(query.keys()) >= 1:
            # It errors when you dont provide anything
            sql = "SELECT * FROM location WHERE {}".format(" AND ".join(qs))
        cur.execute(sql, (*query.values(),))
        db_locations = cur.fetchall()
        conn.close()

        return db_locations

    def update(id, **data) -> dict:
        [conn, cur] = get_db()
        cols = ", ".join(k + "=?" for k in data.keys())
        sql = "UPDATE location SET %s WHERE id=?" % (cols)
        cur.execute(
            sql,
            (
                *data.values(),
                id,
            ),
        )
        conn.commit()
        conn.close()

        return Location.get(id)

    def delete(id: str):
        [conn, cur] = get_db()
        sql = "DELETE FROM location WHERE id=?"
        cur.execute(sql, (id,))
        conn.commit()
        conn.close()


class Booking:
    def new(**data) -> dict:
        parsed_data = {
            "id": nanoid.generate(),
            "status": "PENDING",
            "checkin_date": data["checkin_date"],
            "checkout_date": data["checkout_date"],
            "location_id": data["location_id"],
            "user_id": data["user_id"],
        }
        [conn, cur] = get_db()
        cols = ", ".join(parsed_data.keys())
        placeholders = ":" + ", :".join(parsed_data.keys())
        sql = "INSERT INTO booking (%s) VALUES (%s)" % (cols, placeholders)
        cur.execute(sql, parsed_data)
        conn.commit()
        conn.close()

        return parsed_data

    def get(id: str) -> None | dict:
        [conn, cur] = get_db()
        cur.execute("SELECT * FROM booking WHERE id=?", (id,))
        db_booking = cur.fetchone()
        joined_booking = dict(db_booking)
        location = Location.get(db_booking["location_id"])
        review = Review.getAll(booking_id=db_booking["id"], no_join=True)
        joined_booking["review"] = None
        user = User.get(db_booking["user_id"])
        if len(review) != 0:
            joined_booking["review"] = review[0]
        joined_booking["location"] = location
        joined_booking["user"] = user
        conn.close()

        return joined_booking

    def getAll(**query) -> None | list:
        qs = []
        review_none = False
        for key, val in query.items():
            if key == "review" and val == None:
                review_none = True
                continue
            qs.append("{}=?".format(key))
        if "review" in query:
            del query["review"]
        [conn, cur] = get_db()
        sql = "SELECT * FROM booking"
        if len(query.keys()) >= 1:
            # It errors when you dont provide anything
            sql = sql + " WHERE {}".format(" AND ".join(qs))
        cur.execute(sql, (*query.values(),))
        db_bookings = cur.fetchall()
        joined_bookings = []
        for booking in db_bookings:
            joined_booking = dict(booking)
            user = User.get(booking["user_id"])
            location = Location.get(booking["location_id"])
            review = Review.getAll(booking_id=booking["id"], no_join=True)
            joined_booking["review"] = None
            if len(review) != 0 and not review_none:
                joined_booking["review"] = review[0]
            joined_booking["location"] = location
            joined_booking["user"] = user
            joined_bookings.append(joined_booking)

        conn.close()

        return joined_bookings

    def update(id, **data) -> dict:
        [conn, cur] = get_db()
        cols = ", ".join(k + "=?" for k in data.keys())
        sql = "UPDATE booking SET %s WHERE id=?" % (cols)
        cur.execute(
            sql,
            (
                *data.values(),
                id,
            ),
        )
        conn.commit()
        conn.close()

        return Booking.get(id)


class Review:
    def new(**data) -> dict:
        parsed_data = {
            "id": nanoid.generate(),
            "rating": data["rating"],
            "comment": data["comment"],
            "user_id": data["user_id"],
            "booking_id": data["booking_id"],
        }
        [conn, cur] = get_db()
        cols = ", ".join(parsed_data.keys())
        placeholders = ":" + ", :".join(parsed_data.keys())
        sql = "INSERT INTO review (%s) VALUES (%s)" % (cols, placeholders)
        cur.execute(sql, parsed_data)
        conn.commit()
        conn.close()

        return parsed_data

    def get(id: str) -> None | dict:
        [conn, cur] = get_db()
        cur.execute("SELECT * FROM review WHERE id=?", (id,))
        db_review = cur.fetchone()
        joined_review = dict(db_review)
        user = User.get(db_review["user_id"])
        joined_review["user"] = user
        conn.close()

        return db_review

    def getAll(**query) -> None | list:
        qs = []
        no_join = False
        for key, val in query.items():
            if key == "no_join":
                no_join = val
                continue
            qs.append("{}=?".format(key))
        if "no_join" in query:
            del query["no_join"]
        [conn, cur] = get_db()
        sql = "SELECT * FROM review"
        if len(query.keys()) >= 1:
            # It errors when you dont provide anything
            sql = sql + " WHERE {}".format(" AND ".join(qs))
        cur.execute(sql, (*query.values(),))
        db_reviews = cur.fetchall()
        joined_reviews = []
        for review in db_reviews:
            joined_review = dict(review)
            if not no_join:
                review = Booking.get(review["booking_id"])
                joined_review["booking"] = review
            user = User.get(review["user_id"])
            joined_review["user"] = user
            joined_reviews.append(joined_review)

        conn.close()

        return joined_reviews
