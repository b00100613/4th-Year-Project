# File name:/api/init_challenges.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module is used to populate the database.

from api.challenge import Challenge
from models import (ConfigModel, UserModel, challengeModel,
                    User1Model, User6Model,
                    User7Model)
from config import db, basedir
import json
import bcrypt  # third party bcrypt module used to hash and salt passwords
import secrets  # third party secrets module used to generate secrets

challenge_list = []


def setup():  # this function gets called when the flask app starts
    # all previous infomation stored in the database is deleted
    challengeModel.query.delete()
    ConfigModel.query.delete()

    db.session.commit

    # opening JSON file that contains the challenge descriptions
    f = open(basedir+'/api/challenge_desc.json')

    challenges = json.load(f)
    # create a list to store the challenge information from the json file
    for challenge in challenges:
        challenge_input = (challengeModel(title=challenge["title"],
                           description=challenge["description"],
                           difficulty=challenge["difficulty"],
                           challenge_type=challenge["challenge_type"]))
        db.session.add(challenge_input)
        db.session.commit()
    # generate challenge configuration for each challenge.
    # anto is the weak jwt secret used in challenge 3
    challenges_config = [[get_secret(), True, get_secret(), False],
                         [get_secret(), False, get_secret(), False],
                         ["anto", True, get_secret(), False],
                         [get_secret(), True, get_secret(), False],
                         [get_secret(), True, get_secret(), False],
                         [get_secret(), True, get_secret(), False],
                         [get_secret(), True, get_secret(), False]]
    for config_input in challenges_config:
        # update the challenge_config table with the configuration
        config_input = ConfigModel(secret=config_input[0],
                                   jwt_verify=config_input[1],
                                   flag=config_input[2],
                                   solved=config_input[3])
        db.session.add(config_input)
        db.session.commit()
    result = ConfigModel.query.all()
    for challenge in result:
        # create challenge objects based on the data in the challenge list
        challenge_list.append(Challenge(challenge.id,
                                        challenge.secret,
                                        challenge.jwt_verify))
    reset_user_db()


def reset_user_db():
    # user tables are deleted upon start up due so all changes are removed
    UserModel.query.delete()
    User1Model.query.delete()
    User6Model.query.delete()
    User7Model.query.delete()

    # all admin password are generated using secrets apart from chal 1
    admin_password = hash_password(secrets.token_urlsafe(21))
    # users are given a password of a standard users
    user_password = hash_password("userpassword1")
    # admin weak password is the root cause of the vulnerability in chal 1
    admin_weak_password = hash_password("anthony")

    # setup the users in each user table
    challenge_user1 = UserModel("admin",
                                admin_password, "admin", "anto")
    challenge_user2 = UserModel("user1",
                                user_password, "user", "george")

    challenge1_user1 = User1Model("admin",
                                  admin_weak_password,
                                  "admin", "anto")
    challenge1_user2 = User1Model("user1",
                                  user_password, "user", "george")

    challenge6_user1 = User6Model("admin",
                                  admin_weak_password,
                                  "admin", "anto")
    challenge6_user2 = User6Model("user1",
                                  user_password, "user", "george")

    challenge7_user1 = User7Model("admin",
                                  admin_password, "admin", "anto")
    challenge7_user2 = User7Model("user1",
                                  user_password, "user", "george")

    db.session.add_all([challenge_user1, challenge_user2])
    db.session.add_all([challenge1_user1, challenge1_user2])
    db.session.add_all([challenge6_user1, challenge6_user2])
    db.session.add_all([challenge7_user1, challenge7_user2])
    db.session.commit()


def hash_password(password):
    """this function uses the bcrypt module to salt and hash password before
    they are stored in the database."""
    password = password
    # passwords must be utf-8 encoded before being salted or hashed.
    bytePassword = password.encode('utf-8')
    password_salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(bytePassword, password_salt)
    return password_hash


def get_secret():
    """this function uses the secrets module to generate
    cryptographically strong secret"""
    return secrets.token_urlsafe(32)
