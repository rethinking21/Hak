from google.oauth2 import credentials
from UniNotifModule.Google.Credentials import ABCcreds
import pickle
import os


class GoogleCredentialsPickle(ABCcreds.ABCGoogleCredentials):
    def __init__(self):
        self.__creds: credentials.Credentials
        self.path: str = ""
        self.name: str = ""

    def set_path(self, path: str):
        self.path = path

    def set_name(self, name: str):
        self.name = name

    def load(self):
        with open(os.path.join(self.path, self.name), "rb") as fr:
            self.__creds: credentials.Credentials = pickle.load(fr)

    def save(self):
        with open(os.path.join(self.path, self.name), "wb") as fw:
            pickle.dump(self.__creds, fw)

    def get_creds(self) -> credentials.Credentials:
        return self.__creds

    def set_creds(self, cred: credentials.Credentials):
        self.__creds = cred

    def destroy(self):
        os.remove(os.path.join(self.path, self.name))

    def valid_cred(self) -> bool:
        return self.__creds.valid

# encrypt https://stackoverflow.com/questions/69242465/how-to-encrypt-a-pickled-file-in-python
# https://hazarddev.tistory.com/77
