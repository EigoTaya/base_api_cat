import json
from os import access

class AccessInfo:
    # fixed
    # __grant_type = ''
    # __client_id = ''
    # __client_secret = ''
    # __redirect_url = ''

    # valiable
    # __code = ''
    # __access_token = ''

    def __init__(self, file_uri):
        o = open(file_uri, 'r')
        r_data = json.load(o)
        self.__grant_type = r_data['grant_type']
        self.__client_id = r_data['client_id']
        self.__client_secret = r_data['client_secret']
        self.__redirect_uri = r_data['redirect_uri']
        self.__code = None
        self.__access_token = None
        del r_data, o

    # getter
    @property
    def grant_type(self):
        return self.__grant_type

    @property
    def client_id(self):
        return self.__client_id

    @property
    def client_secret(self):
        return self.__client_secret

    @property
    def redirect_uri(self):
        return self.__redirect_uri

    @property
    def code(self):
        return self.__code

    @property
    def access_token(self):
        return self.__access_token

    # setter
    @code.setter
    def code(self, code):
        self.__code = code
        return

    @access_token.setter
    def access_token(self, access_token):
        self.__access_token = access_token
        return
