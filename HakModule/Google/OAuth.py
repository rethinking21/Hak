from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow


class GoogleOAuthGenerator:
    def __init__(self):
        self.client_secret_path: str = ""
        self.redirect_uri: str = r"https://www.google.com/"

        self.scopes = []
        self.services: list = []  # thinking

        self.__flow: Flow

        self.__authorization_url: str = ''
        self.__state: str = ''
        self.__setFlow: bool = False

    def fetch_token_url(self, url):
        pass

    def set_flow(self):  # more
        self.__flow = Flow.from_client_secrets_file(
            self.client_secret_path,
            scopes=self.scopes
        )
        self.__flow.redirect_uri = self.redirect_uri
        self.__setFlow = True

    def create_authorization_url(self):
        # thinking setting
        self.__authorization_url, self.__state = self.__flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='true'
        )

    def get_authorization_url(self) -> str:
        return self.__authorization_url

    def fetch_token_authorization_response(self, url: str):
        self.__flow.fetch_token(authorization_response=url)

    def get_credentials(self) -> credentials.Credentials:
        return self.__flow.credentials


class GoogleOAuthBuilder:
    def __init__(self):
        self.manager: GoogleOAuthGenerator = GoogleOAuthGenerator()

    def set_client_secret_path(self, path: str):
        self.manager.client_secret_path = path
        return self

    def set_redirect_uri(self, url: str):
        self.manager.redirect_uri = url
        return self

    def add_scope(self, scope: str):
        self.manager.scopes.append(scope)
        return self

    def add_scope_calendar(self):
        self.manager.scopes.append('https://www.googleapis.com/auth/calendar')
        return self

    def build(self):
        return self.manager
