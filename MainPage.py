from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for,redirect,session, make_response, Response,config
import os
from Manager import Manager

app = Flask(__name__)
# run the app connecting with the flask
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/',methods=['POST','GET'])
def manage():
    m = Manager()
    result = m.get_all()
    return render_template('manage.html',data = result)

@app.route('/deleteFlight',methods=['POST','GET'])
def deleteFlight():
    if request.method == 'POST':
        FID = request.form.get('FID')
        m = Manager();
        m.delete_flight(FID)
        return redirect('/deleteFlight')
    else:
        return render_template('DeleteFlight.html')

@app.route('/addFlight',method=['POST'])
def addFlight():
    if request.method == 'POST':
        FlightNumber = request.form.get("FlightNumber")
        Airplane = request.form.get("Airplane")
        Airline = request.form.get("Airline")
        deptTime = request.form.get("deptTime")
        deptAirport = request.form.get("deptAirport")
        arrTime = request.form.get("arrTime")
        arrAirport = request.form.get("arrAirport")
        Price = request.form.get("Price")
        AvailableSeats = request.form.get("AvailableSeats")





if __name__=='__main__':
    app.run(debug=True)

