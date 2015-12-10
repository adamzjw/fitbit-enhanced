__author__ = 'adamzjw'

import urllib, urllib2
import base64
import webbrowser
import json


class Token:
    def __init__(self, tokenStr):
        tokenDict = json.loads(tokenStr)
        self.access_token = tokenDict.get('access_token', None)
        self.expires_in = tokenDict.get('expires_in', None)
        self.refresh_token = tokenDict.get('refresh_token', None)
        self.scope = tokenDict.get('scope', None)
        self.user_id = tokenDict.get('user_id', None)
        self.token = None

class Client:
    def __init__(self, clientID, clientSecret):
        self.clientID = clientID
        self.clientSecret = clientSecret

    def get_encodedSecret(self):
        return base64.b64encode("%s:%s" % (self.clientID, self.clientSecret))

    def get_token(self):
        return self.token

    def obtainConsent(self):
        body = {
                'response_type' : 'code',
                'redirect_uri': 'http://adamzjw.github.io/',
                'client_id': self.clientID,
                'scope': 'activity nutrition heartrate location nutrition profile settings sleep social weight',
                }

        data = urllib.urlencode(body)
        auth_url = 'https://www.fitbit.com/oauth2/authorize?'

        webbrowser.open(auth_url + data, new=2)

        authrizedCode = raw_input("Pls provide the code: ").strip()

        if len(authrizedCode) == 0:
            raise ValueError("AuthrizedCode is empty")
        else:
            self.authrizedCode = authrizedCode

    def requestToken(self):
        encodedSecret = self.get_encodedSecret()
        token_url = 'https://api.fitbit.com/oauth2/token'

        body = {
                'grant_type' : 'authorization_code',
                'redirect_uri': 'http://adamzjw.github.io/',
                'client_id': self.clientID,
                'code': self.authrizedCode,
                }

        headers = { 'Authorization': 'Basic %s' % encodedSecret, 'Content-Type': 'application/x-www-form-urlencoded'}

        data = urllib.urlencode(body)
        request = urllib2.Request(token_url, data, headers)

        try:
            response = urllib2.urlopen(request)
            tokenStr = response.read()
            self.token = Token(tokenStr)
        except urllib2.URLError, e:
            print e.code
            print e.read()