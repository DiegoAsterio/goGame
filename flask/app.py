import pprint

import json

from flask import Flask, render_template, session, request, redirect

from pickleshare import *
db = PickleShareDB('miDB')

from pymongo import MongoClient

client = MongoClient("mongo", 27017)
mongodb= client.goPlayers

app = Flask(__name__)
app.secret_key = b'2V2XNWcP0L4rD2vKykr69rlBmnYkAAzdpn2gBwFHNKE='

def getCountries():
    try:
        fn = open("./static/slim-3.json","U")
    except IOError:
        return ["Something went wrong"]
    ISO3166 = json.load(fn)
    ret = []
    for country in ISO3166:
        ret.append(country['alpha-3'])
    return ret
    

def addusername():
    params = dict()
    if 'email' in session:
        params['email'] = session['email']
    return params

def valid_user(name):
    if not name in db:
        return True
    return False

def check_name(name):
    if mongodb.ugonet.count_documents({'key_name':name}) > 0:
        return False
    else:
        return True
                                  

@app.before_request
def before_request():
    if not 'history' in session:
        session['history'] = [None, None, None]
    session['history'].insert(0,request.path)
    session['history'] =  session['history'][0:3] 

@app.route('/')
def print_index():
    params = addusername()
    params['history'] = session['history'][0:3]
    return render_template('index.html',params=params)

@app.route('/ratings')
def print_ratings():
    params = addusername()
    return render_template('ratings.html',params=params)

@app.route('/about')
def print_about():
    params=addusername()
    return render_template('about.html',params=params)

@app.route('/contact')
def print_contact():
    params=addusername()
    return render_template('contact.html',params=params)

@app.route('/register', methods=['POST', 'GET'])
def print_reg():
    params=addusername()
    params['error'] = None
    if request.method == 'POST':
        user = request.form['exampleInputEmail1']
        passwd = request.form['exampleInputPassword1']
        if valid_user(user):
            db[user] = {'pass': passwd}
            return redirect('/')
        else:
            params['error'] = 'Username already chosen'
    return render_template('register.html', params=params)

def valid_login(name, passw):
    if name in db:
        return passw == db[name]['pass']
    return False

@app.route('/login', methods=['POST', 'GET'])
def print_login():
    params = addusername()
    params['error'] = None
    params['user'] = None
    if request.method == 'POST':
        params['user'] = request.form['exampleInputEmail1']
        passwd = request.form['exampleInputPassword1']
        if valid_login(params['user'],passwd):

            session['email']=request.form['exampleInputEmail1']
            return redirect('/')
        else:
            params['error'] = 'Invalid username/password'
    return render_template('login.html',params=params)
    
@app.route('/logout')
def erase_session():
    session.clear()
    return redirect('/')

@app.route('/statistics')
def show_statistics():
    params = addusername()
    numberOfSpaniards = mongodb.ugonet.count_documents({"citizenship":"ESP"})
    vals = mongodb.ugonet.find({"citizenship":"ESP"})
    pprint.pprint(vals)
    names = []
    for i in range(numberOfSpaniards):
        names.append(vals[i]['key_name'])
    params['names'] = names
    return render_template('statistics.html',params=params)
    
@app.route('/documents', methods=['POST', 'GET'])
def show_docs():
    params = addusername()
    playersAdded = mongodb.ugonet.find({"creator":params['email']})
    params['names'] = []
    params['countries'] = getCountries()
    for player in playersAdded:
        name = player['key_name']
        params['names'].append(name)
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        citizenship = request.form['citizenship']
        if check_name(name):
            mongodb.ugonet.insert({
                'key_name' : name,
                'sex' : sex,
                'citizenship' : citizenship,
                'creator' : params['email']
                })
            return redirect('/documents')
        else:
            params['error'] = "Introduced player already exists"
    return render_template('documents.html',params=params)

@app.route('/erase', methods=['POST'])
def erase_player():
    pprint.pprint(request.form)
    name = request.form['erasename']
    mongodb.ugonet.remove({'key_name':name})
    return redirect('/documents')
    
    

@app.route('/mongo')
def mongo():
    val = mongodb.ugonet.find_one()
    pprint.pprint(val)
    numberOfSpaniards = mongodb.ugonet.count_documents({"citizenship":"ESP"})
    return val['key_name']
    
