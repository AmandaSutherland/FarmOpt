# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
# import gss
# import pygal
# import json
# from urllib2 import urlopen  # python 2 syntax
# from pygal.style import DarkSolarizedStyle


# create our little application :)
app = Flask(__name__)
app.config.from_object('app_config')
# app.config.from_envvar('FARMOPT_SETTINGS', silent=True)

# sqlite3 /home/selina/Documents/SoftDes/FarmOptDB/farmopt.db < schema.sql

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

@app.route('/login', methods=['GET', 'POST'])
# @login_required
def login():
	error = None
	if request.method == 'POST':
		print 'Username type:', type(request.form['username'])
		cur = g.db.execute('select username, password from users order by id desc')
		users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
		for user in users:
			if request.form['username'] == user['username']:
				if request.form['password'] == user['password']:
					session['logged_in'] = True
					flash('You are logged in')
					return redirect(url_for('crops'))
				else:
					error = 'Invalid password'
		if error == None:
			error = 'Invalid username'
	return render_template('login.html', error=error)

@app.route('/signup', methods=['GET','POST'])
def signup():
	error = None
	if request.method == 'POST':
		cur = g.db.execute('select username, password from users order by id desc')
		users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
		for user in users:
			if request.form['username'] == user['username']:
				if request.form['password'] == user['password']:
					session['logged_in'] = True
					flash('You already signed up')
					return redirect(url_for('crops'))
				else:
					error = 'Unavailable username, choose a different one'
		if error == None:
			g.db.execute('insert into users (username, password) values (?, ?)',
				 [request.form['username'], request.form['password']])
			g.db.commit()
			session['logged_in'] = True
			flash('You are successfully signed up')
			return redirect(url_for('crops'))
	return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('crops'))

def optimizion():
	print 'I am optimizing'
	results = ()
	# Do the math!
	# Inputs: User_Schedule and Crop_Hours are nested lists, available hours is a list
	# Output: Tuple of lists and nested list
	results = farmsum(User_Schedule, Crop_Hours, Available_Hours)


if __name__ == '__main__':
	init_db()
	app.run()
