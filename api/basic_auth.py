# File name:basic_auth.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module handles the basic authentication in challenge 1

# The flask extension flask_httpauth is used to check the authoriztion header
from flask_httpauth import HTTPBasicAuth
from models import ConfigModel, User1Model
import bcrypt

# an instance for the HTTPBasicAuth class is defined
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    # the verify password decorator is called in the API routes.py file
    # the challenge1users table is queried.
    results = User1Model.query.filter_by(username=username).first()
    if results is not None:
        """bcrypt function is used to compare password
        in request to hashed password"""
        if bcrypt.checkpw(password.encode("utf-8"), results.password) is True:
            # if the credential are valid the username is returned
            return username
        else:
            return False
    else:
        return False


@auth.error_handler
def auth_error(status):
    """this decorator is used to handle http response error if the credentials
    are not valid"""
    return {"Error": "Access Denied"}, status   # JSON error message return


def get_account(username):
    """this is a custom function that takes in the username returned from the
    verify_password function and gets the user account details associated
    with it"""
    results = User1Model.query.filter_by(username=username).first()
    if results is not None:
        # if the username is not admin then only return the account information
        if results.username != "admin":
            return {"username": results.username,
                    "role": results.role,
                    "name": results.name}, 200
        else:
            # if username is admin then return the information and the flag
            result = (
                      ConfigModel.query.filter(ConfigModel.id
                                               == 1).one_or_none())
            flag = result.flag
            return {"username": results.username,
                    "role": results.role, "name":
                    results.name, "flag": flag}, 200
    else:
        # if the username doesnt exist in the table then return false.
        return False
