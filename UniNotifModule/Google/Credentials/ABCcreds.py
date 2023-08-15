from google.oauth2 import credentials
from abc import *


class ABCGoogleCredentials(metaclass=ABCMeta):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get_creds(self) -> credentials.Credentials:
        pass

    @abstractmethod
    def set_creds(self, cred: credentials.Credentials):
        pass
