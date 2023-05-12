# File name:/api/jwt_token.py
# Student id:B00100613
# Student Name: Anthony Yalcin
# University: Technological University Dublin Blanchardstown Campus.
# Purpose: this module handles the encoding and decoding of the jwt token

import jwt
import datetime


# init the challenge class
class jwt_token:

    def __init__(self, username, role, secret):
        # JWT class has three attributes
        self.username = username
        self.role = role
        self.secret = secret

    def encode_token(self):
        # the username, role and the timestamp are the three claims
        # the secret is used to sign the jwt token
        token = jwt.encode({'user': self.username,
                            'role': self.role,
                            'exp': datetime.datetime.utcnow() +
                            datetime.timedelta(minutes=10)}, self.secret)
        return token

    def decode_token(access_token, jwt_verify, secret):
        """setting the verify signature to false is the root cause of
        the vulnerability in challenge 2"""
        if jwt_verify is False:
            decoded = jwt.decode(access_token, options={"verify_signature":
                                                        False})
        else:
            # all other challenges enforce verification
            decoded = jwt.decode(access_token, secret, algorithms="HS256")
        return decoded
