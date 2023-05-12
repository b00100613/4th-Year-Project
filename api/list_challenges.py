# File name: /api/list_challenges.py
# Student id: B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module is used to get the list of challenges from the db

from models import challengeModel


# get_all returns a list of challenges from the db
def get_all():
    challenge_list = []
    result = challengeModel.query.all()
    for challenge in result:
        challenge_list.append({"id": str(challenge.id),
                              "title": challenge.title,
                               "difficulty": challenge.difficulty})
    return challenge_list, 200

# get challenge returns the challenge information based on the id parsed
def get_challenge(id):
    result = challengeModel.query.filter(challengeModel.id == id).one_or_none()
    if result is not None:
        return {"title": result.title, "description": result.description}, 200
    else:
        return {"message": "Invalid challenge ID"}, 404
