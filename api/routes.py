# File name:/api/routes.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module handles the API routes

from flask import Blueprint, request, send_from_directory
import config
import api.list_challenges
import api.challenge
import api.basic_auth
from api.init_challenges import challenge_list
"""This module is used when the end user browses to the web application
each route is a page in the web application or depending on the id in the url
"""


api_blueprint = Blueprint(
    'api_blueprint', __name__
)  # create an blueprint object for the API


@api_blueprint.route("/api/challenges", methods=["GET"])
@config.limiter.exempt
def challenges():
    # this endpoint will return the list of challenges
    try:
        return api.list_challenges.get_all()
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>", methods=["GET"])
@config.limiter.exempt
def challenge(id):
    """this endpoint will return the challenge based on the id submitted
    if the id does not exist it will return a 404 error"""
    try:
        id = int(id)
        return api.list_challenges.get_challenge(id)
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>/login", methods=["POST"])
@config.limiter.limit("100 per minute")
def post_login(id):
    """this endpoint is used to log into each challenge exlcuding
    challenge 1 as this is handled by another function"""
    try:
        id = int(id)
        if id > 1 and id < 8:
            return challenge_list[id-1].login(request)
        else:
            return {"message": "resource does not exist"}, 404
    except:
        return {"message":
                "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>/account", methods=["GET", "PUT"])
@config.limiter.exempt
def account(id):
    """this endoint allows both GET and PUT methods,
    GET eturns the account information based on the id
    PUT will update the account information"""
    user_id = None
    try:
        id = int(id)
        if request.method == "GET":
            try:
                user_id = request.headers["X-USER-ID"]
            except:
                user_id = None
            if id > 0 and id < 8:
                return challenge_list[id-1].get_account(request, user_id)
            else:
                return {"message": "resource does not exist"}, 404
        elif request.method == "PUT":
            if id > 0 and id < 8:
                return challenge_list[id-1].update_account(request)
            else:
                return {"message": "resource does not exist"}, 404
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>/account/<user_id>", methods=["GET"])
@config.limiter.exempt
def get_user_account_id(id, user_id):
    # this endpoint returns the user account information base on the id
    try:
        id = int(id)
        try:
            if id == 4:
                return challenge_list[id-1].get_account(request, user_id)
            else:
                return {"message": "resource does not exist"}, 404
        except:
            return {"message": "Error check request and try again"}, 400
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>/submit_flag", methods=["POST"])
@config.limiter.limit("100 per minute")
def challenge_submit(id):
    # this endpoint returns submits the flag based on the id
    try:
        id = int(id)
        request_data = request.get_json()
        flag = request_data["flag"]
        if id > 0 and id < 8:
            return challenge_list[id-1].submit_flag(flag)
        else:
            return {"message": "resource does not exist"}, 404
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>/status", methods=["GET"])
@config.limiter.exempt
def challenge_status(id):
    # this endoint returns the staus of the challenge based on the id
    try:
        id = int(id)
        if id > 0 and id < 8:
            return challenge_list[id-1].check_status()
        else:
            return {"message": "resource does not exist"}, 404
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/<id>/reset", methods=["POST"])
@config.limiter.limit("100 per minute")
def challenge_reset(id):
    # this endpoint resets the status of the challenge based on the id
    try:
        id = int(id)
        request_data = request.get_json()
        reset = request_data["reset"]
        if id > 0 and id < 8:
            return challenge_list[id-1].reset_challenge(reset)
        else:
            return {"message": "resource does not exist"}, 404
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/challenge/1/protected", methods=["GET"])
@config.limiter.exempt
@api.basic_auth.auth.login_required
def basic_auth_protected():
    """this endpoint handdle the protected resource for challenge 1
    it requires basic authentication in order to access it"""
    try:
        return api.basic_auth.get_account(api.basic_auth.auth.current_user())
    except:
        return {"message": "Error check request and try again"}, 400


@api_blueprint.route("/api/download/postman", methods=["GET"])
@config.limiter.exempt
def download_postman():
    # this endpoints downloads the postman collection
    try:
        return send_from_directory(config.upload_folder,
                                   "Vulnerable_API_Postman.zip",
                                   as_attachment=True)
    except:
        return {"message": "An error has occure please check the request"}, 400


@api_blueprint.route("/api/download/commonpasswords", methods=["GET"])
@config.limiter.exempt
def download_wordlist():
    # this endpoints downloads the postman collection
    try:
        return send_from_directory(config.upload_folder,
                                   "commonpasswords.txt",
                                   as_attachment=True)
    except:
        return {"message": "An error has occure please check the request"}, 400


@api_blueprint.route("/api/challenge/<id>/admin", methods=["GET"])
@config.limiter.exempt
def admin_get(id):
    """this endpoint is one of the hidden endpoints in challenge 6
    it returns a message to the client with another endpoint"""
    try:
        id = int(id)
        if id == 6:
            return challenge_list[id-1].get_admin(request)
        else:
            return {"message": "resource does not exist"}, 404
    except:
        return {"message": "An error has occure please check the request"}, 400


@api_blueprint.route("/api/challenge/<id>/admin/account/update",
                     methods=["PUT"])
@config.limiter.limit("100 per minute")
def admin_update_account(id):
    try:
        """this endpoint is another hidden endpoint as part of challenge 6
        it allows users to update their account information"""
        id = int(id)
        if id == 6:
            return challenge_list[id-1].update_account(request)
        else:
            return {"message": "resource does not exist"}, 404
    except:
        return {"message": "Error check request and try again"}, 400
