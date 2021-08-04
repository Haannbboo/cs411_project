from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for, redirect

import pymysql

mydb = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='veGryq-roccab-tawsi5',
    database='test', )

mycursor = mydb.cursor()

# sql = "SELECT * FROM Flights WHERE carrier_name = 'Delta Air Lines' "
# mycursor.execute(sql)
# myresult = mycursor.fetchall()

# app = Flask(__name__)
# Base = declarative_base()
# engine1 = create_engine('mysql+pymysql://root:david0811@localhost:3306/Airports')
# DBSession = sessionmaker(bind=engine1)

try:
    SQL = "DROP TRIGGER insertTrig;"
    mycursor.execute(SQL)
except pymysql.err.OperationalError:
    pass
# SET @flight = (SELECT id FROM flights WHERE FlightNumber = new.FlightNumber AND deptTime = new.deptTime);
insertTrig = """
CREATE TRIGGER insertTrig
    BEFORE INSERT ON flights
    FOR EACH ROW
    BEGIN
        IF EXISTS(SELECT id FROM flights WHERE FlightNumber = new.FlightNumber AND deptTime = new.deptTime) THEN
            SIGNAL SQLSTATE '45000';
        END IF;
        IF @flight IS NULL THEN
            SET @maxID = (SELECT MAX(id) FROM flights);
            SET new.id = @maxID + 1;
        END IF;
    END;
"""
mycursor.execute(insertTrig)


class Manager():

    def __init__(self):
        pass

    def get_all(self):
        SQL = "SELECT * from flights"
        mycursor.execute(SQL)
        return mycursor.fetchall()

    def delete_flight(self, fid: int):
        cursor = mydb.cursor()
        SQL = "DELETE FROM flights WHERE id = " + str(fid)
        print(SQL)
        cursor.execute(SQL)
        mydb.commit()

    def add_flight(self, form: dict):
        cursor = mydb.cursor()
        # cursor.execute("SELECT MAX(id) FROM flights")
        # max_id = cursor.fetchone()[0]

        # fid = max_id + 1
        FlightNumber = form.get("FlightNumber", "")
        Airplane = form.get("Airplane", "")
        Airline = form.get("Airline", "")
        deptTime = form.get("deptTime", "")
        deptAirport = form.get("deptAirport", "")
        arrTime = form.get("arrTime", "")
        arrAirport = form.get("arrAirport", "")
        Price = form.get("Price", "")
        AvailableSeats = form.get("AvailableSeats", 0)

        SQL = "INSERT INTO flights VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, 0)".format(FlightNumber,
                                                                                                           Airplane,
                                                                                                           Airline,
                                                                                                           deptTime,
                                                                                                           deptAirport,
                                                                                                           arrTime,
                                                                                                           arrAirport,
                                                                                                           Price,
                                                                                                           AvailableSeats,)
        print(SQL)
        try:
            cursor.execute(SQL)
            mydb.commit()
            return True
        except pymysql.err.OperationalError as e:
            if e.args[0] == 1644:  # signal 45000
                return False
            else:
                print(e)

    def edit_flight(self, fid: int, form: dict):
        # Input: request.form
        # Output: True - success; False - incorrect data failed (condition tested in SQL trigger)
        dict_cursor = mydb.cursor(cursor=pymysql.cursors.DictCursor)
        dict_cursor.execute("SELECT * FROM flights WHERE id = " + str(fid))
        flight = dict_cursor.fetchall()
        assert len(flight) == 1
        flight = flight[0]

        FlightNumber = form.get("FlightNumber", flight.get("FlightNumber"))
        Airplane = form.get("Airplane", flight.get("Airplane"))
        Airline = form.get("Airline", flight.get("Airline"))
        deptTime = form.get("deptTime", flight.get("deptTime"))
        deptAirport = form.get("deptAirport", flight.get("deptAirport"))
        arrTime = form.get("arrTime", flight.get("arrTime"))
        arrAirport = form.get("arrAirport", flight.get("arrAirport"))
        Price = form.get("Price", flight.get("Price"))
        AvailableSeats = form.get("AvailableSeats", flight.get("AvailableSeats"))

        SQL = "UPDATE flights SET FlightNumber = '{FlightNumber}', Airplane = '{Airplane}', Airline = '{Airline}', deptTime = '{deptTime}', deptAirport = '{deptAirport}', arrTime = '{arrTime}', arrAirport = '{arrAirport}', Price = '{Price}', AvailableSeats = {AvailableSeats} WHERE id = {fid};".format(
            FlightNumber=FlightNumber, Airplane=Airplane, Airline=Airline, deptTime=deptTime, deptAirport=deptAirport,
            arrTime=arrTime, arrAirport=arrAirport, Price=Price, AvailableSeats=AvailableSeats, fid=fid)
        print(SQL)
        mycursor.execute(SQL)
        mydb.commit()
        return True


m = Manager()
# m.edit_flight(0, {'Price': 100, 'FlightNumber': 123, 'AvailableSeats': 20})
m.add_flight(
    {'FlightNumber': 'HB9999', 'Airplane': 'Airbus 999', 'Airline': 'HB Airline', 'deptTime': '2021-09-01 12:25',
     'deptAirport': 'CKX', 'arrTime': '2021-09-01 15:55', 'arrAirport': 'XYZ', 'Price': '9999', 'AvailableSeats': 120})
# m.delete_flight(6)
