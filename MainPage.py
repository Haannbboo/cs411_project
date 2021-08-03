from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for,redirect,session, make_response, Response,config
import os

app = Flask(__name__)
# run the app connecting with the flask
app.config['SECRET_KEY'] = os.urandom(24)

Base = declarative_base()
engine1 = create_engine('mysql+pymysql://root:davidxiong@localhost:3306/Airports')
DBSession = sessionmaker(bind = engine1)

import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'david0811',
    database = 'Airports',)

mycursor = mydb.cursor()



if __name__=='__main__':
    app.run(debug=True)

