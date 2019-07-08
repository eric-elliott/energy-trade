from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps
import pandapower as pp
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = '5bbfc192a5ca109222100a16832db52d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['GOOGLEMAPS_KEY'] = 'AIzaSyDOC-Pa8ZuHUASQUgJT6llCFaSedrzsD2Q'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# GoogleMaps(app)

from soltrade.powergrid import PowerGrid
powergrid = PowerGrid()

from soltrade import routes