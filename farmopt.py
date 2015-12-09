# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from contextlib import closing
import pygal
import json
from urllib2 import urlopen  # python 2 syntax
from pygal.style import DarkSolarizedStyle
# from flask_googlelogin import GoogleLogin
# from flask_login import LoginManager, login_required

# from flask.ext.rauth import RauthOAuth2
# from app_config import *

# create our little application :)
app = Flask(__name__)
app.config.from_object('app_config')
# googlelogin = GoogleLogin()
# googlelogin.init_app(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# googlelogin = GoogleLogin(app, login_manager)
# FARMOPT_SETTINGS = app_config
# app.config.from_envvar('FARMOPT_SETTINGS', silent=True)

# sqlite3 /tmp/flaskr.db < schema.sql

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # db = g._database = connect_to_database()
        db = g._database = connect_db()
    db.row_factory = sqlite3.Row
    return db
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# @app.route('/')
# def show_entries():
#     cur = g.db.execute('select title, text from entries order by id desc')
#     entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
#     return render_template('show_entries.html', entries=entries)

@app.route('/')
def crops():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('crop_page.html', entries=['please', 'link', 'me'], crop_dictionary={'carrots': '3', 'beans': '2'})

@app.route('/chart')
def plot_chart(date='20140415', state='IA', city='Ames'):
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    line_chart = line_chart.render()
    return render_template('plot.html', line_chart=line_chart)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('crops'))

@app.route('/disp_user')
def display_user():
	user = query_db('select * from users where username = ?',
	                [the_username], one=True)
	if user is None:
	    print 'No such user'
	else:
	    print the_username, 'has the id', user['user_id']

# @app.route('/oauth2callback')
# @googlelogin.oauth2callback
# def create_or_update_user(token, userinfo, **params):
#     user = User.filter_by(google_id=userinfo['id']).first()
#     if user:
#         user.name = userinfo['name']
#         user.avatar = userinfo['picture']
#     else:
#         user = User(google_id=userinfo['id'],
#                     name=userinfo['name'],
#                     avatar=userinfo['picture'])
#     db.session.add(user)
#     db.session.flush()
#     login_user(user)
#     return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
# @login_required
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('crops'))
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You already signed up')
            return redirect(url_for('crops'))
    return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    init_db()
    app.run()