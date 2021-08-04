from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for, redirect

import hashlib

import pymysql

mydb = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    database='test', )

mycursor = mydb.cursor()


# sql = "SELECT * FROM Flights WHERE carrier_name = 'Delta Air Lines' "
# mycursor.execute(sql)
# myresult = mycursor.fetchall()


# app = Flask(__name__)
# Base = declarative_base()
# engine1 = create_engine('mysql+pymysql://root:david0811@localhost:3306/Airports')
# DBSession = sessionmaker(bind = engine1)

class User():
    def __init__(self):
        pass

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

    def QueryByFlightNum(self, flightNumber, date) -> dict:
        # Assume each flight has EXACTLY ONE ENTRY
        # Input: flightNumber
        # Output: dict
        btime = date + ' 00:00'
        etime = date + ' 23:59'
        SQL = "SELECT * FROM flights WHERE FlightNumber='{}' AND deptTime BETWEEN '{}' AND '{}'".format(flightNumber, btime, etime)
        print(SQL)

        cursor = mydb.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(SQL)
        flight = cursor.fetchall()
        assert len(flight) == 1
        # print(flight)
        return flight[0]

    def Book(self, primary_key):
        # R, W
        pass

    def UnBook(self, primary_key):
        pass


u = User()
u.QueryByFlightNum("PN6213", "2021-08-12")
