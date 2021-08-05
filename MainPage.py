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

@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        u = User()
        username = request.form.get('username')
        password = request.form.get('psw')
        result = u.log_in(username,password)
        if result[0] == 0:
            return result[1]
        if result[0] == 0.5:
            return "You Need To Sign Up For An Account"
        else:
            session['username'] = username;
            if result[1] == "user":
                return redirect('/user')
            else:
                return redirect('/manage')
    else:
        return render_template('Login.html')


@app.route('/signup',methods=['POST','GET'])
def sign_up():
    if request.method == "POST":
        u = User()
        result = u.register(request.form)
        if result[0] == 0:
            return result[1]
        else:
            return redirect('/')
    else:
        return render_template('SignUp.html')


@app.route('/user',methods=['POST','GET'])
def user():
    u = User()
    if request.method == 'POST':
        if request.form['btn'] == 'Query':
            fromLocation = request.form.get('from')
            toLocation = request.form.get('to')
            Date = request.form.get('date')
            return render_template('result.html', data = u.QueryByLocationDate(fromLocation,toLocation,Date))
        else:
            FID = request.form.get('fid')
            session["FID"] = FID
            return redirect("/Book")
    else:
        return render_template('result.html',data = u.get_all(), name=session.get('username'))

@app.route('/manage',methods=['POST','GET'])
def manage():
    m = Manager()
    result = m.get_all()
    print(result)
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
    if request.method == 'POST':
        if request.form['btn'] == 'No':
            return redirect('/Book')
        else:
            u = User(session.get('username'))
            u.Book(session.get('FID'),666)
            return redirect('/user')
    else:
        FID = session.get('FID')
        u = User()
        return render_template('booking.html',data = u.QueryByFID(FID))

'''
@app.route('/edit', methods=['POST','GET'])
def edit():
'''



if __name__=='__main__':
    app.run(debug=True)

