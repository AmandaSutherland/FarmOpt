'''
Farming Optimization Project
Authors: Amanda Sutherland, Mimi Kome, Ziyu (Selina) Wang
Current Function: Takes user input intuitively
'''

# Construct a nested list from user input
# turn it into a dictionary
from flask import Flask, render_template, request, bort, redirect, url_for
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
def index():
	return 'Index Page'

@app.route('/hello')
def hello():
	return 'Hello World'

@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))

@app.errorhandler(404)
def page_not_found(error):
    return make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp

#To access parameters submitted in the URL (?key=value) you can use the args attribute:
searchword = request.args.get('key', '')

with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'POST'
    print url_for('static', filename='style.css')
# def collectingData():
# 	print 'Hello there! Welcome to FarmOpt!\nWould you like to continue? (y/n)'
# 	openSoftware = raw_input()
# 	if openSoftware == 'n':
# 		print 'Bye!'
# 	elif openSoftware == 'y':
# 		print 'How many kinds of crops are you planning on planting?'
# 		numCrops = raw_input()
# 		crops = []
# 		print 'How many weeks are you planning on planting all of these crops?'
# 		numWeeks = raw_input()
# 		weeks = []

# 		for crop in range(int(numCrops)):
# 			individualcrop = []
# 			weeks.append(individualcrop)
# 			print 'What is the name of the', str(crop+1), 'st crop?'
# 			crops.append(raw_input())
# 			for week in range(int(numWeeks)):
# 				print 'How much of', crops[crop], 'would you like to plant in week', str(week+1), '?'
# 				weeks[crop].append(raw_input())
# 		print 'Here is all the data we received!'
# 		for crop in range(int(numCrops)):
# 			print crops[crop], ':', str(weeks[crop])
			


if __name__ == '__main__':
	app.debug = True
	app.run()