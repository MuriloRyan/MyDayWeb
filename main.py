from flask import Flask, render_template,request, redirect, session
from flask_session import Session
from database.userconfig import User
import database.mongodb as db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_KEY') 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

""" ___________________ """
"""                     """
""" FRONTEND OPERATIONS """
""" ___________________ """
@app.route('/')
def homepage():
    if 'email' in session:
        email = session['email']
        taskdata = db.getTask({'email': email})
        return render_template('home.html', taskdata=taskdata)
    else:
        return render_template('home.html', notConnected=True)

@app.route('/profile')
def profile():

    return render_template('profile.html')

@app.route('/user/mytasks/', methods=['GET', 'POST'])
def taskPage():

    taskname = request.args.get('taskname')

    AllTasks = db.getTask({'email': session['email']})
    for task in AllTasks:
        if task['taskname'] == taskname:
            TaskData = task

    return render_template('taskpage.html',taskdata=TaskData)

@app.route('/newtask')
def newtask():

    return render_template('newtask.html')

@app.route('/auth/login/new')
def loginPage():

    return render_template('login.html')

@app.route('/auth/register/new')
def signUpPage():

    return render_template('signup.html')

@app.route('/auth/checksession')
def checkSession():
    try:
        session['email']

        return redirect('/profile')
    except:
        return redirect('/auth/login/new')

""" __________________ """
"""                    """
""" BACKEND OPERATIONS """
""" __________________ """
@app.route('/auth/register/api/mongodb',methods=["POST"])
def databaseSignUp():
    
    data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password']
           }

    toSignUp = User(data['username'],data['email'],data['password'])
    db.signIn(toSignUp.get_data())

    return redirect('/auth/login/new')

@app.route('/auth/login/api/mongodb', methods=["POST"])
def databaseLogin():
    data = {
        'email': request.form['email'],
        'password': request.form['password']
    }

    toLogIN = User('__null__', data['email'], data['password'])
    tryData = db.logIn(toLogIN.get_data())

    if tryData is not None:
        session['username'] = db.findIn({'username'}, data['email'])['username']
        session['email'] = data['email']
        session['sessionhash'] = tryData
        return redirect('/')
    else:
        return redirect('/auth/login/new')

@app.route('/function/session/exit')
def sessionExit():
    session.clear()
    
    return redirect('/')

@app.route('/function/api/mongodb/newtask', methods=["POST"])
def databseNewTask():

    taskname = request.form['newTaskName']
    taskcomment = request.form['newTaskComment']

    db.addTask({'email': session['email']},{'taskname': taskname,'comment': taskcomment})

    return redirect('/')

@app.route('/function/api/mongodb/killtask/', methods=["POST"])
def databaseKillTask():

    taskToKill = request.args.get('taskname')

    db.killTask({'email': session['email']},taskToKill)

    return redirect('/')

if __name__ == '__main__':
    app.run()
