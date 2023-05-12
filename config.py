# File name:config.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this modules holds the configuration for the app and extentions

import os  # os module needed to get the file directory
from flask_sqlalchemy import SQLAlchemy  # module needed for RL database
from flask import Flask
from flask_limiter import Limiter  # module needed for rate limiting
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# create new limiter object to and store the configuration
limiter = Limiter(
    get_remote_address,
    app=app,
    # currently this amount is set to a high value for testing purposes
    default_limits=["1000000 per day", "1000000 per hour"],
    storage_uri="memory://",
)
# gets the folder location on the system, so no full path names are required
basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = basedir+"/api/uploads"


class DbConfig(object):
    # create the DbConfig class and store the location of the db.
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+basedir+"/challenges.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(DbConfig)

db = SQLAlchemy(app)
