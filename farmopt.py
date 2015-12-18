# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash, Response
from contextlib import closing
from datetime import date
# import gss
# import pygal
# import json
# from urllib2 import urlopen  # python 2 syntax
# from pygal.style import DarkSolarizedStyle

DATABASE = '/tmp/flaskr.db'
# create our little application :)
app = Flask(__name__)
app.config.from_object('app_config')
# app.config.from_envvar('FARMOPT_SETTINGS', silent=True)

# sqlite3 /home/selina/Documents/SoftDes/FarmOptDB/farmopt.db < schema.sql
# Global Variables
seasonstartdate = date.today()
totalweeks = int
laborhours = int

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

@app.route('/')
def crops():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	cur1 = g.db.execute('select cropname, startweek, numbeds, numweeks from crops where username = ?', [session['username']])
	crops = [dict(cropname=row[0], startweek=row[1], numbeds=row[2], numweeks=row[3]) for row in cur1.fetchall()]
	cur2 = g.db.execute('select weeks, hours, seasonstartdate from weeks where username = ?', [session['username']])
	weeks = [dict(weeks=row[0], hours=row[1], seasonstartdate=row[2]) for row in cur2.fetchall()]
	cur3 = g.db.execute('select cropname, process, pweeks, phours from processes where username = ?', [session['username']])
	processes = [dict(cropname=row[0], process=row[1], pweeks=row[2], phours=row[3]) for row in cur3.fetchall()]
	return render_template('crop_page.html', crops=crops, weeks=weeks, processes=processes, totalweeks=len(weeks), selectedweeks=[])

@app.route('/weeks')
def weeks():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	cur1 = g.db.execute('select cropname, startdate, numbeds from crops where username = ?', [session['username']])
	crops = [dict(cropname=row[0], startdate=row[1], numbeds=row[2]) for row in cur1.fetchall()]
	cur2 = g.db.execute('select id, hours from weeks where username = ?', [session['username']])
	weeks = [dict(id=row[0], hours=row[1]) for row in cur2.fetchall()]
	return render_template('crop_page.html', crops=crops, weeks=weeks, selectedweeks=[], numweeks=len(weeks))

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

@app.route('/addcrop', methods=['POST'])
def add_crop():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into crops (username, cropname, startweek, numbeds, numweeks) values (?, ?, ?, ?, ?)',
				 [session['username'], request.form['cropname'], request.form['startweek'], request.form['numbeds'], request.form['numweeks']])
	g.db.commit()
	flash('New crop was successfully added')
	return redirect(url_for('crops'))

@app.route('/addweeks', methods=['POST'])
def add_weeks():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute("delete from weeks where username = ?", [session['username']])
	g.db.execute('insert into weeks (username, weeks, hours, seasonstartdate) values (?, ?, ?, ?)',
				 [session['username'], request.form['weeks'], request.form['hours'], request.form['seasonstartdate']])
	g.db.commit()
	seasonstartdate = request.form['seasonstartdate']
	totalweeks = int(request.form['weeks'])
	laborhours = int(request.form['hours'])
	flash('Labor information was successfully registered')
	return redirect(url_for('crops'))

@app.route('/addprocess', methods=['POST'])
def add_process():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into processes (username, cropname, process, pweeks, phours) values (?, ?, ?, ?, ?)',
					 [session['username'], request.form['selected'], request.form['process'], request.form['selectedweeks'], request.form['phours']])
	g.db.commit()
	flash('New process was successfully added')
	return redirect(url_for('crops'))

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
	print 'I am calculating'
	cur1 = g.db.execute('select cropname, startdate, numbeds, numweeks from crops where username = ?', [session['username']])
	crops = [dict(cropname=row[0], startdate=row[1], numbeds=row[2], numweeks=row[3]) for row in cur1.fetchall()]
	cur2 = g.db.execute('select id, hours from weeks where username = ?', [session['username']])
	weeks = [dict(id=row[0], hours=row[1]) for row in cur2.fetchall()]
	cur3 = g.db.execute('select cropname, process, pweeks, phours from processes where username = ?', [session['username']])
	processes = [dict(cropname=row[0], process=row[1], pweeks=row[2], phours=row[3]) for row in cur3.fetchall()]
	# for crop in crops:
	# 	startweek = (crop.startdate - seasonstartdate)/7
	# 	g.db.execute('insert into weeks (startweek) values (?)',
	# 				 [startweek])
	# Do the math!
	# Inputs: User_Schedule and Crop_Hours are nested lists, available hours is a list
	# Output: Tuple of lists and nested list
	results = farmsum(User_Schedule, Crop_Hours, Available_Hours)
	hour_schedule = results[2]
	farm_death = results[1]
	weekly_sum = results[0]

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		print 'Username type:', type(request.form['username'])
		cur = g.db.execute('select username, password from users order by id desc')
		users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
		for user in users:
			if request.form['username'] == user['username']:
				if request.form['password'] == user['password']:
					session['username'] = request.form['username']
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
					session['username'] = request.form['username']
					session['logged_in'] = True
					flash('You already signed up')
					return redirect(url_for('crops'))
				else:
					error = 'Unavailable username, choose a different one'
		if error == None:
			g.db.execute('insert into users (username, password) values (?, ?)',
				 [request.form['username'], request.form['password']])
			g.db.commit()
			session['username'] = request.form['username']
			session['logged_in'] = True
			flash('You are successfully signed up')
			return redirect(url_for('crops'))
	return render_template('signup.html', error=error)

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('crops'))


if __name__ == '__main__':
	init_db()
	app.run()
