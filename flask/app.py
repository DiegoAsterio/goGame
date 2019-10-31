import pprint

from flask import Flask, render_template, session, request, redirect

from pickleshare import *
db = PickleShareDB('miDB')

app = Flask(__name__)
app.secret_key = b'2V2XNWcP0L4rD2vKykr69rlBmnYkAAzdpn2gBwFHNKE='

@app.before_request
def before_request():
    if not 'history' in session:
        session['history'] = [None, None, None]
    session['history'].insert(0,request.path)
    session['history'] =  session['history'][0:3] 

@app.route('/')
def print_index():
    email = None
    if 'email' in session:
        email = session['email']
    return render_template('index.html',email=email, P1=session['history'][0],P2=session['history'][1],P3=session['history'][2])

@app.route('/ratings')
def print_ratings():
    return render_template('ratings.html')

@app.route('/about')
def print_about():
    return render_template('about.html')

def valid_user(name):
    if not name in db:
        return True
    return False

@app.route('/register', methods=['POST', 'GET'])
def print_reg():
    error = None
    user = None
    if request.method == 'POST':
        user = request.form['exampleInputEmail1']
        passwd = request.form['exampleInputPassword1']
        if valid_user(user):
            db[user] = {'pass': passwd}
            return redirect('/')
        else:
            error = 'Username already chosen'
    return render_template('register.html', user=user, regerror=error)

def valid_login(name, passw):
    if name in db:
        return passw == db[name]['pass']
    return False

@app.route('/login', methods=['POST', 'GET'])
def print_login():
    error = None
    user = None
    if request.method == 'POST':
        if valid_login(request.form['exampleInputEmail1'],
                       request.form['exampleInputPassword1']):
            session['email']=request.form['exampleInputEmail1']
            return redirect('/')
        else:
            error = 'Invalid username/password'
        user = request.form['exampleInputEmail1']
    return render_template('login.html',loginerror=error,user=user)
    
@app.route('/logout')
def erase_session():
    session.clear()
    return redirect('/')
