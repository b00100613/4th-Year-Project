# File name:/client/routes.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module handles the client routes
"""This module is used when the end user browses to the web application
each route is a page in the web application or depending on the id in the url
"""


from flask import Blueprint, render_template
import config

client_blueprint = Blueprint(
    'client_blueprint', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='/client/static'
)  # create an blueprint object for the API


@client_blueprint.route("/", methods=["GET"])
@config.limiter.exempt
def index():
    # returns the index page or if there is an error the error page
    try:
        return render_template("index.html")
    except:
        return render_template("error.html"), 404


@client_blueprint.route("/challenges", methods=["GET"])
@config.limiter.exempt
def challenges_list():
    # returns the challenges page or if there is an error the error page
    try:
        return render_template("challenges.html")
    except:
        return render_template("error.html"), 404


@client_blueprint.route("/challenge/<id>", methods=["GET"])
@config.limiter.exempt
def challenge_get(id):
    # returns the challenges page based on the <id> in the URL path
    try:
        id = int(id)
        if id <= 7 and id > 0:
            if id != 1:
                return render_template("jwt_challenge.html")
            elif id == 1:
                return render_template("basic_auth_challenge.html")
            else:
                return render_template("error.html"), 404
        else:
            return render_template("error.html"), 404
    except:
        return render_template("error.html"), 404


@client_blueprint.route("/challenge/<id>/account", methods=["GET"])
@config.limiter.exempt
def challenge_protected(id):
    # returns the challenge account page based on the <id> in the URL path
    try:
        id = int(id)
        if id <= 7 and id > 0:
            if id > 1 and id != 4:
                return render_template("jwt_challenge_account.html"), 200
            elif id == 4:
                return render_template("challenge_4_account.html"), 200
            elif id == 1:
                return render_template("basic_auth_account.html"), 200
            else:
                return render_template("error.html"), 404
        else:
            return render_template("error.html"), 404
    except:
        return render_template("error.html"), 404


@client_blueprint.route("/challenge/<id>/admin", methods=["GET"])
@config.limiter.exempt
def admin_get(id):
    # returns the admin page in challenge 6
    try:
        if id == 6:
            return render_template("admin.html"), 200
        else:
            return render_template("error.html"), 404
    except:
        return render_template("error.html"), 404
