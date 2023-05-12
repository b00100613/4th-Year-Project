# File name:models.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module declares the db models for each table

from config import db


class challengeModel(db.Model):
    # model for the challenges table
    __tablename__ = "challenges"
    # id is primary key so it can be linked with the challenges_config table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    description = db.Column(db.String(32))
    difficulty = db.Column(db.String(32))
    challenge_type = db.Column(db.String(32))

    def __init__(self, title, description, difficulty, challenge_type):
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.challenge_type = challenge_type


class ConfigModel(db.Model):
    # model for the challenges_config table
    __tablename__ = "challenges_config"
    # id is foreign key so it can be linked with the challenges table
    id = db.Column(db.Integer, db.ForeignKey(challengeModel.id),
                   primary_key=True, autoincrement=True)
    secret = db.Column(db.String(32))
    jwt_verify = db.Column(db.Boolean)
    flag = db.Column(db.String(32))
    solved = db.Column(db.Boolean)

    def __init__(self, secret, jwt_verify, flag, solved):
        self.secret = secret
        self.jwt_verify = jwt_verify
        self.flag = flag
        self.solved = solved


"""3 seperate user tables are declared and initialized as
certain details will change depending on the challenge chosen
challenge 1 and challenge 7 require users to update table contents
one user table is not ideal as changes to one challenge will affect another."""


class UserModel(db.Model):
    __tablename__ = "challenge_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, username, password, role, name):
        self.username = username
        self.password = password
        self.role = role
        self.name = name


class User1Model(db.Model):
    __tablename__ = "challenge1_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, username, password, role, name):
        self.username = username
        self.password = password
        self.role = role
        self.name = name


class User6Model(db.Model):
    __tablename__ = "challenge6_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, username, password, role, name):
        self.username = username
        self.password = password
        self.role = role
        self.name = name


class User7Model(db.Model):
    __tablename__ = "challenge7_users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __init__(self, username, password, role, name):
        self.username = username
        self.password = password
        self.role = role
        self.name = name
