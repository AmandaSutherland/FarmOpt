# Running FarmOpt

1) Clone the repo. <br />
2) Go through the steps below to get heroku up and running. <br />
3) Install all the following: <br />
	Flask==0.10.1 (through http://flask.pocoo.org/docs/0.10/installation/) <br />
	gunicorn==19.4.1 <br />
	itsdangerous==0.24 <br />
	Jinja2==2.8 <br />
	MarkupSafe==0.23 <br />
	Werkzeug==0.11.2 <br />
	wheel==0.24.0 <br />
4) Run the program locally by running 'python farmopt.py' or go to the web version at 'farmoptimization.heroku.com'

# Further information on FarmOpt 
	http://farmoptproject.weebly.com/

# python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application support the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started
$ pip install -r requirements.txt
$ createdb python_getting_started
$ heroku local:run python manage.py migrate
$ python manage.py collectstatic
$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master
$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
