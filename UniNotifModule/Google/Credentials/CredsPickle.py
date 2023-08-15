from google.oauth2 import credentials
import ABCcreds
import pickle


class GoogleCredentialsPickle(ABCcreds):
    def __init__(self):
        self.__creds: credentials.Credentials

    def load(self):
        pass

    def save(self):
        pass

    def get_creds(self) -> credentials.Credentials:
        return self.__creds

    def set_creds(self, cred: credentials.Credentials):
        self.__creds = cred


