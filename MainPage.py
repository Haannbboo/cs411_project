from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, url_for,redirect,session, make_response, Response,config
import os
from Manager import Manager
from User import User

app = Flask(__name__)
# run the app connecting with the flask
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/user',methods=['POST','GET'])
def user():
    u = User()
    if request.method == 'POST':
        fromLocation = request.form.get('from')
        toLocation = request.form.get('to')
        Date = request.form.get('date')
        return render_template('result.html', data = u.QueryByLocationDate(fromLocation,toLocation,Date))
    else:
        return render_template('result.html',data = u.get_all())


@app.route('/',methods=['POST','GET'])
def manage():
    m = Manager()
    result = m.get_all()
    return render_template('manage.html',data = result)

@app.route('/deleteFlight',methods=['POST','GET'])
def deleteFlight():
    if request.method == 'POST':
        FID = request.form.get('FID')
        print(FID)
        m = Manager()
        m.delete_flight(FID)
        return redirect('/deleteFlight')
    else:
        return render_template('DeleteFlight.html')


@app.route('/addFlight',methods=['POST','GET'])
def addFlight():
    if request.method == 'POST':
        m = Manager()
        m.add_flight(request.form)
        return redirect('/addFlight')
    else:
        return render_template('AddFlight.html')

@app.route('/Book',methods=['POST','GET'])
def book():
    return "book"

'''
@app.route('/edit', methods=['POST','GET'])
def edit():
'''



if __name__=='__main__':
    app.run(debug=True)

