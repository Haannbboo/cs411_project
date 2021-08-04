from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for, redirect

import hashlib
import time

import pymysql
from pymysql.constants import CLIENT

mydb = pymysql.connect(
    host='35.202.82.204',

    user='root',
    passwd='uiuccs411',
    database='flightBookingDatabase',
    client_flag=CLIENT.MULTI_STATEMENTS)

mycursor = mydb.cursor()

# SQL for addNewUser
# STARTS HERE
try:
    SQL = "DROP TRIGGER addNewUser;"
    mycursor.execute(SQL)
except pymysql.err.OperationalError:
    pass

addNewUserTrig = """
CREATE TRIGGER addNewUser
    BEFORE INSERT ON users
    FOR EACH ROW
    BEGIN
        IF EXISTS(SELECT uid FROM users WHERE username = new.username) THEN
            SIGNAL SQLSTATE '45000';
        END IF;
        IF EXISTS(SELECT uid FROM users WHERE email = new.email) THEN
            SIGNAL SQLSTATE '45000';
        END IF;
        SET @maxID = (SELECT MAX(uid) FROM users);
        IF @maxID IS NULL THEN
            SET @maxID = 0;
        END IF;
        SET new.uid = @maxID + 1;
    END;
"""
mycursor.execute(addNewUserTrig)
# ENDS HERE


# SQL for addBookingTrig
# STARTS HERE
try:
    SQL = "DROP TRIGGER addBookingTrig;"
    mycursor.execute(SQL)
except pymysql.err.OperationalError:
    pass

addBookingTrig = """
CREATE TRIGGER addBookingTrig
    BEFORE INSERT ON bookings
    FOR EACH ROW
    BEGIN
        SET @seats = (SELECT AvailableSeats FROM flights WHERE id = new.fid);
        IF @seats < 1 THEN
            SIGNAL SQLSTATE '45000';
        END IF;
        SET @maxID = (SELECT MAX(bid) FROM bookings);
        IF @maxID IS NULL THEN
            SET @maxID = 0;
        END IF;
        SET new.bid = @maxID + 1;
    END;
"""
mycursor.execute(addBookingTrig)
# ENDS HERE

class User():
    def __init__(self):
        self.username = None
        self.pwdhash = None

        self.uid = -1

    def get_user_info(self, uid: int):
        SQL = "SELECT * FROM users WHERE uid = {};".format(uid)
        cursor = mydb.cursor()
        cursor.execute(SQL)
        result = cursor.fetchall()
        if len(result) == 0:
            print("uid not in database")
            return None
        return result[0]

    def log_in(self, username: str, password: str):
        pwdhash = hashlib.md5(password.encode("utf-8")).hexdigest()

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM users WHERE username = '{}';".format(username))
        userinfo = cursor.fetchall()

        if len(userinfo) == 0:
            # username not in the database
            # redirect to register
            return 0.5, 'need_register'
        else:
            # username in the database
            assert len(userinfo) == 1
            userinfo = userinfo[0]

        if pwdhash != userinfo[2]:
            # password incorrect
            return 0, 'incorrect_password'
        else:
            self.uid = userinfo[0]
            self.pwdhash = pwdhash
            self.username = username
            return 1, userinfo[3]

    def register(self, form: dict):
        # need to redirect to log_in page to log in again
        # form: request.form
        username = form.get("username", "user"+hashlib.md5(str(time.time()).encode('utf-8')).hexdigest())
        password = form.get("password")
        password_rec = form.get("password_rec")
        email = form.get("email")
        roll = form.get("roll", "user")

        if password is None or password_rec is None:
            return 0, "no_password"
        if password != password_rec:
            return 0, "password_mismatch"

        # check email and username repetition

        pwdHash = hashlib.md5(password.encode('utf-8')).hexdigest()

        cursor = mydb.cursor()
        SQL = "INSERT INTO users VALUES (1, '{}', '{}', '{}', '{}')".format(username, pwdHash, roll, email)
        print(SQL)
        try:
            cursor.execute(SQL)
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1644:
                return 0, "username_exists"
            else:
                print(e)
        mydb.commit()


        return 1, "success"



    def get_all(self):
        SQL = "SELECT * from flights"

    def QueryByLocationDate(self, fromLocation, toLocation, date, order="time"):
        # Date: '2021-01-01'
        # Location: 'PKX' (IATA code)
        # Default ordering: order by deptTime
        btime = date + ' 00:00'
        etime = date + ' 23:59'

        orderby = ""
        if order == "time":
            orderby = " ORDER BY deptTime"
        if order == "price":
            orderby = " ORDER BY Price DESC"

        SQL = "SELECT * FROM flights WHERE deptAirport='{}' AND arrAirport='{}' AND deptTime BETWEEN '{}' AND '{}'{};".format(
            fromLocation, toLocation, btime, etime, orderby)
        print(SQL)
        cursor = mydb.cursor()
        cursor.execute(SQL)

        result = cursor.fetchall()
        return result

    def QueryByFID(self, FID):
        SQL = "SELECT * FROM test WHERE id='{}';".format(FID)
        cursor = mydb.cursor()
        cursor.execute(SQL)
        result = cursor.fetchall()
        return result

    def QueryByFlightNum(self, flightNumber, date) -> dict:
        # Assume each flight has EXACTLY ONE ENTRY
        # Input: flightNumber
        # Output: dict
        btime = date + ' 00:00'
        etime = date + ' 23:59'
        SQL = "SELECT * FROM flights WHERE FlightNumber='{}' AND deptTime BETWEEN '{}' AND '{}'".format(flightNumber,
                                                                                                        btime, etime)
        print(SQL)

        cursor = mydb.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(SQL)
        flight = cursor.fetchall()
        assert len(flight) == 1
        # print(flight)
        return flight[0]

    def Book(self, fid: int, bookPrice: int):
        # R, W
        if self.uid is None:
            return False

        SQL = """
        START TRANSACTION;
        SET @currPrice = (SELECT Price FROM flights WHERE id = {});
        INSERT INTO bookings VALUES (-1, {}, {}, @currPrice, (SELECT NOW() FROM DUAL), 1);
        UPDATE flights SET AvailableSeats=AvailableSeats-1 WHERE id = {};
        COMMIT;
        """.format(fid, self.uid, fid, fid)
        print(SQL)
        cursor = mydb.cursor()
        try:
            cursor.execute(SQL)
            mydb.commit()
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1644:
                mydb.rollback()
                return False
        return True

    def checkBooking(self):

        SQL = """
        SELECT deptTime, FlightNumber FROM flights LEFT OUTER JOIN bookings ON flights.id = bookings.fid WHERE uid = {} ORDER BY deptTime
        """.format(self.uid)
        print(SQL)
        cursor = mydb.cursor()
        cursor.execute(SQL)
        result = cursor.fetchall()
        print(result)
        return result


    def UnBook(self, fid: int):
        return


u = User()
u.log_in("hb", "123456")
# u.QueryByFlightNum("PN6213", "2021-08-12")
print(u.Book(1, 1000000000))
# u.checkBooking()

# u.register({"username": "hb", "password": "123456", "password_rec": "123456", "email": "hb@uiuc.edu", "roll": "manager"})