# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from app_config import *

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)