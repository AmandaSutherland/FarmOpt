# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
# from app_config import *

# configuration
DATABASE = '/tmp/farmopt.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
# FARMOPT_SETTINGS = app_config
# app.config.from_envvar('FARMOPT_SETTINGS', silent=True)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()