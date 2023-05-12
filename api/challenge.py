# File name:/api/challenge.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: core logic and functions surrounding the challenges

from api.jwt_token import jwt_token  # import jwt_token
# importing the db models from models.py
from models import (ConfigModel,  UserModel, User6Model, User7Model)
from config import db  # need to query and update the db in certain challenges
import bleach  # third party module used to sanitize strings
import bcrypt  # used in this module to check the password when login()


class Challenge:  # init the challenge class
    # initialize the challenge class,  it takes 3 arguments.
    def __init__(self, id, secret, jwt_verify):
        self.id = id
        self.secret = secret
        self.jwt_verify = jwt_verify
    # Perform a login,  takes in the request from routes.py

    def login(self, request):
        # from the request it gets the json request body key values
        json_data = request.get_json(force=True)
        username = json_data['username']
        password = json_data['password'].encode('utf-8')
        id = self.id

        """check the challenge id and query the users table depending on what
        id was parsed,if a valid is parsed the check if the username exists."""

        if id > 1 or id < 6:
            results = UserModel.query.filter_by(username=username).first()
            """check if challenge id = 2-6 as they all use the same db
            model UserModel"""

        elif id == 7:
            """challenge 7 uses the db model "User7Model" as it requires user
            to update contents of the db."""
            results = User7Model.query.filter_by(username=username).first()

        elif id == 1:
            """if the challenge id = 1 then return an error message as this
            login is handled by another function"""
            return {"message": "resource does not exist"}, 404

        if results is None:
            """if the username in the request does not match one in the
            database then return a 401 error."""
            return {"message": "Invalid Credentials"}, 401

        else:
            """if the username exist compare the password in the request with
            the password for that user in the database.
            using the bcrypt checkpw function as the passwords in the
            database are salted and hashed."""
            if bcrypt.checkpw(password, results.password) is True:
                # create a jwt_token object, returns a jwt_token string
                access_token = jwt_token(results.username,
                                         results.role,
                                         self.secret)

                # encode the access_token string with the jwt encode function.
                access_token = access_token.encode_token()

                """if the challenge id is equal to 4. as challenge 4 is the
                only challenge when the user_id json key-value pair is
                returned to the user to be used in another request if the
                challenge id is not equal to 4 or 5 then only the access_token
                is return"""
                if id != 4 and id != 5:
                    return {"access_token": access_token}, 200
                else:
                    return {"access_token": access_token,
                            "user_id": results.id}, 200
            else:
                """if the password in the request does not match the password
                for that particular user then return an error message."""
                return {"message": "Invalid Credentials"}, 401

    """the check_auth function check the authorization header in the request
    to see if it is valid.this function gets called by the get_account and
    update account functions."""
    def check_auth(self, request):
        # declare and initatize the decode_access_token function
        try:
            # gets the jwt_token from the authorization header.
            access_token = request.headers.get(
                                               'Authorization', ''
                                               ).split(' ')[1]
            # calls the decode function from jwt_token.py
            decoded_token = jwt_token.decode_token(
                                                   access_token,
                                                   self.jwt_verify,
                                                   self.secret)
            return decoded_token  # returns the decoded_token
        except:
            return False

    """this function takes in the the request from routes.py and calls the
    check_auth() function to see the jwt token is valid. if the jwt_token is
    valid then query one of the user tables depending on the challenge id
    check if the jwt_token has role claim set to admin and if so return
    the user details and the flag.
    else return only the user details."""
    def get_account(self, request, user_id):
        id = self.id
        # call the check_auth function to see if jwt_token is valid.
        decoded_token = self.check_auth(request)

        if decoded_token is not False:
            """check if challenge id = 2-5 as they all use the same
            db model UserModel"""
            if id > 1 and id < 6:
                """if user id is present then return the account details
                associated with the id"""
                if user_id is not None and (id == 4 or id == 5):
                    if id == 4:
                        """checks if the user is trying to use the header
                        from challenge 5 in challenge 4"""
                        if "X-USER-ID" in request.headers:
                            return {"message":
                                    "this header cant be used here"}, 400
                        else:
                            user_result = (
                                           UserModel.query.filter(
                                                                  UserModel.id
                                                                  == user_id
                                                                  )
                                           .one_or_none())

                    elif id == 5:
                        user_result = UserModel.query.filter(
                                                             UserModel.id ==
                                                             user_id
                                                             ).one_or_none()
                else:
                    """if user id is not present then return the account
                    details associated with the JWT token"""
                    user_result = UserModel.query.filter(
                                                         UserModel.username ==
                                                         decoded_token["user"]
                                                         ).one_or_none()
            elif id == 7:
                """challenge 7 uses the db model User7Model as it requires
                user to update contents of the db"""
                user_result = User7Model.query.filter(
                                                      User7Model.username ==
                                                      decoded_token["user"]
                                                      ).one_or_none()
            else:
                user_result = User6Model.query.filter(
                                                      User6Model.username ==
                                                      decoded_token["user"]
                                                      ).one_or_none()
            # check if the role claim in the jwt_token is = "admin"
            if decoded_token["role"] == "admin" or user_result.role == "admin":
                result = ConfigModel.query.filter(
                                                  ConfigModel.id == id
                                                  ).one_or_none()
                flag = result.flag
                # if it is equal to admin return the user info + flag
                return {"username": str(user_result.username),
                        "role": str(user_result.role),
                        "flag": flag, "name": user_result.name}, 200
            else:
                # else only return the user information
                return {"username": str(user_result.username),
                        "role": str(user_result.role),
                        "name": user_result.name}, 200
        else:
            #  return an error message if the decoded_token is not valid.
            return {"message": "JWT Token is not valid"}, 401

    """this function check the status of the challenge by querying the config
    table in the database this is a boolean value if false challenge is not
    solve,  if true then the challenge is solved"""
    def check_status(self):
        id = self.id
        # query the config table
        result = ConfigModel.query.filter(ConfigModel.id == id).one_or_none()
        if result is not None:
            if result.solved is False:
                # if the solved column is set to False then return not solved
                return {"message": "Challenge not solved"}, 200
            else:
                # if the challenge has been solved then return solved
                return {"message": "Challenge solved"}, 200
        else:
            # if the challenge id does not exist return an error
            return {"message": "Invalid challenge ID"}, 404

    """this function gets called when a client sends a request to POST
    /api/challenge/{id}/submit_flag endpoint.
    it takes one arguent which is the flag value from the request body."""
    def submit_flag(self,  flag):
        # checks to see if the flag matches one in the database.
        result = ConfigModel.query.filter(
                                          ConfigModel.flag == flag
                                          ).one_or_none()
        # if there is a match then solved column for that challenge to True.
        if result is not None:
            result.solved = True
            db.session.commit()
            return {"message": "Solved"}, 200
        else:
            # else return an error message
            return {"message": "Invalid flag"}, 400

    """this function gets called when a client sends a GET request to the
    /api/challenge/{id}/reset endpoint. it takes one arguent which is the
    flag value from the request body."""
    def reset_challenge(self, reset):
        from api.init_challenges import reset_user_db, get_secret
        id = self.id
        if reset is True:
            # if reset is equal to try query challenge id
            result = ConfigModel.query.filter(
                                              ConfigModel.id == id
                                              ).one_or_none()
            if result is not None:
                # set the solved column to True,  meaning the lab is solved.
                result.solved = False
                result.flag = get_secret()
                db.session.commit()
                """if the challenge id = 7 then reset the the user database as
                 changes could have been made."""
                if id == 7 or id == 6:
                    # import the reset_user_db function from init_challenges.
                    reset_user_db()
                # if the challenge has been reset return 200 ok message.
                return {"message": "Challenge Reset"}, 200
            else:
                # if the challenge id is not valid then return an error
                return {"message": "Invalid challenge"}, 404
        # if the user submits a false value then do nothing but return message
        elif reset is False:
            return {"message": "challenge not reset"}, 200
        else:
            # returns an error message if anythin other than true is submit
            return {"message":
                    "Invalid option please submit true or false"}, 404

    """this function gets called when a client sends a PUT request to the
    /api/challenge/{id}/reset endpoint. it takes one arguent which is the flag
    value from the request body."""
    def update_account(self, request):
        id = self.id
        # check the user jwt_token is valid
        decoded_token = self.check_auth(request)
        # get the json body key-value pairs from the request
        if request.data:
            request_data = request.get_json()
        else:
            return {"message": "expecting name and role json key-value"}, 400

        for key in request_data:
            # the bleach module is used to clean used to sanitize the input.
            request_data[key] = bleach.clean(request_data[key])

        """check if the decoded access token is not equal to false if it is
        then query the database for that user"""
        if decoded_token is not False:
            """this is the root cause of the challenge 7 vulnerability in
            which the entire user supplied data is inserted into the
            database."""
            if id == 7:
                result = User7Model.query.filter(
                                                 User7Model.username ==
                                                 decoded_token["user"]
                                                 ).one_or_none()
                # if the username exist then update the
                if result is not None:
                    User7Model.query.filter(
                                            User7Model.username ==
                                            decoded_token["user"]
                                            ).update(dict(request_data))
                else:
                    """if the username in the token does not match one in
                    the db return an error"""
                    return {"message": "User does not exist"}, 404
            elif id == 6:
                try:
                    result = (
                            User6Model.query.filter(
                                                    User6Model.username ==
                                                    decoded_token["user"])
                            .one_or_none())
                    # if the username exist then update the
                    if result is not None:
                        role = request_data['role']
                        name = request_data['name']
                        print(name)
                        if role is not None and name is not None:
                            if role == "admin" or role == "user":
                                result.role = role
                                result.name = name
                            else:
                                return {"message": "only user roles are "
                                        "admin and user"}, 400
                    else:
                        """if the username in the token does not match one
                         in the db return an error"""
                        return {"message": """Not allowed user does
                                              not exist"""}, 404
                except:
                    return{
                           "message": """Invalid json key-value pair
                            expecting role and name"""}, 400
            else:
                """return error message if any other challenge id is
                submitted"""
                return {"message": "Invalid challenge id"}, 404
            db.session.commit()
            return {"message": "account updated"}, 200
        else:  # if the jwt_token is invalid return an error
            return {"message": "Not allowed access token invalid"}, 401

    def get_admin(self, request):
        # call the check_auth function to see if jwt_token is valid.
        decoded_token = self.check_auth(request)

        if decoded_token is not False:
            message = ("to update your name and role send a PUT "
                       "request to: "
                       "/api/challenge/6/admin/account/update")
            return {"message": message}
        else:  # if the jwt_token is invalid return an error
            return {"message": "Not allowed access token invalid"}, 401
