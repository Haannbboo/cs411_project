from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for, redirect

import hashlib

import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'david0811',
    database = 'Airports',)

mycursor = mydb.cursor()

sql = "SELECT * FROM Flights WHERE carrier_name = 'Delta Air Lines' "
mycursor.execute(sql)
myresult = mycursor.fetchall()


app = Flask(__name__)
Base = declarative_base()
engine1 = create_engine('mysql+pymysql://root:david0811@localhost:3306/Airports')
DBSession = sessionmaker(bind = engine1)

class User():
    def __init__(self):
        pass

    def get_all(self):
        SQL = "SELECT * from flights"

    def OrderByTime(self):
        pass

    def OrderByPrice(self):
        pass

    def QueryByFlightNum(self):
        pass

    def Book(self,primary_key):
        pass

    def UnBook(self,primary_key):
        pass