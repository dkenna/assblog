import jwt
from jwcrypto import jwk, jwt, jws
import time
from datetime import datetime
import requests
import json

jwks_endpoint = 'http://dkenna.com:8000/get_jwks'

class TokenVerifier:
    """
        verify self-emitted token
    """
    def __init__(self, token):
        self.token = token
        self.errmsg = ""
        self.pubkey = None
        self.jwks = self.get_jwks()

    def get_jwks(self):
        r = requests.get(jwks_endpoint)
        jwks = r.text
        return jwks

    def verify(self):
        """ check if signed by auth server"""
        try:
            token = jwt.JWT(key=self.pubkey, jwt=self.token)
            jwks = jwk.JWKSet()
            jwks.import_keyset(self.jwks)
            jwks = list(jwks)
            key = jwks[0]
            token.token.verify(key)
            claims = json.loads(token.token.payload.decode('utf-8'))
            return claims
        except Exception as e:
            print(type(e))
            print(e)
            self.errmsg = "failed sig verification"
            return None

def test_verifier():
    verifier = TokenVerifier('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJleHAiOjE1NDQ5MDkyMzYsIm5iZiI6MTU0NDkwODYzNiwiaXNzIjoidXJuOmF1dGhuX3NlcnZlciIsImF1ZCI6Imp1ZHkud2Fsc2giLCJpYXQiOjE1NDQ5MDg2MzYsImppdCI6MzIwMDUxMTM1LCJ1c2VybmFtZSI6Imp1ZHkud2Fsc2giLCJzdWIiOiJqdWR5LndhbHNoIiwiZW1haWwiOiJqdWR5LndhbHNoQG1haWwuY29tIiwiZmlyc3RfbmFtZSI6Ikp1ZHkiLCJsYXN0X25hbWUiOiJXYWxzaCIsInR5cCI6ImF1dGgifQ.ha8nnQJBbt433zUqV2m0asY_jpZujV8bEotT8up2Aqr6qFfe0Ea5-OEpQBNbbqikCJs5V_mx2pVz8d8G3Dgk2gvGYkAg-g7KhO8oDzOjxwsNyLDbfr82deoBztQBdpDWzCOvuBBHj3YJF6r0u__PPwGpDTp0kJA0MRiQwVDEUyGmyh89vpLcfw9E2w--latbNidEyVFti9EF0CBGEnKbcjPZG-9VpbxIMLjSbHOdPBmnH8aojyaFY5EqyO_h4kRELx0jOkyEBJnUGaCv5p6QUhcVMbgtmdG5VRRDVRyIb-VrFe7Soq52KfSVgbu9ZEOiNRteTCOdrFG7rUwamoDZww')
    verifier.verify()
