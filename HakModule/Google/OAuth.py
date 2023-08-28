from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow
from typing import Optional


class GoogleOAuthGenerator:
    """
    Class for generating Google OAuth2 authorization URL and credentials.

    Attributes
    ----------
    client_secret_path : str
        Path to the client secret JSON file.
    redirect_uri : str
        Redirect URI for OAuth2 flow.
    scopes : list
        List of OAuth2 scopes.
    services : list
        List of service names associated with the generated credentials.

    Methods
    -------
    fetch_token_url(url)
        Fetch token using the provided URL.
    set_flow()
        Set up OAuth2 flow using client secrets file and scopes.
    create_authorization_url()
        Create the authorization URL for user consent.
    get_authorization_url() -> str
        Get the authorization URL for user consent.
    fetch_token_authorization_response(url)
        Fetch token from the authorization response URL.
    get_credentials() -> credentials.Credentials
        Get the generated credentials.

    """
    def __init__(self):
        """
        Initialize the GoogleOAuthGenerator.
        """
        self.client_secret_path: str = ""
        self.redirect_uri: str = r"https://www.google.com/"

        self.scopes = []
        self.services: list = []  # thinking

        self.__flow: Optional[Flow] = None

        self.__authorization_url: str = ''
        self.__state: str = ''
        self.__setFlow: bool = False

    def fetch_token_url(self, url):
        """
        Fetch token using the provided URL.

        Parameters
        ----------
        url : str
            URL containing the token.

        """
        pass

    def set_flow(self):  # more
        """
        Set up OAuth2 flow using client secrets file and scopes.
        """
        self.__flow = Flow.from_client_secrets_file(
            self.client_secret_path,
            scopes=self.scopes
        )
        self.__flow.redirect_uri = self.redirect_uri
        self.__setFlow = True

    def create_authorization_url(self):
        """
        Create the authorization URL for user consent.
        """
        # thinking setting
        self.__authorization_url, self.__state = self.__flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='true'
        )

    def get_authorization_url(self) -> str:
        """
        Get the authorization URL for user consent.

        Returns
        -------
        str
            Authorization URL.

        """
        return self.__authorization_url

    def fetch_token_authorization_response(self, url: str):
        """
        Fetch token from the authorization response URL.

        Parameters
        ----------
        url : str
            URL containing the token.

        """
        self.__flow.fetch_token(authorization_response=url)

    def get_credentials(self) -> credentials.Credentials:
        """
        Get the generated credentials.

        Returns
        -------
        credentials.Credentials
            Generated credentials.

        """
        return self.__flow.credentials


class GoogleOAuthBuilder:
    """
    Builder class for constructing GoogleOAuthGenerator instances.

    Methods
    -------
    set_client_secret_path(path)
        Set the client secret file path.
    set_redirect_uri(url)
        Set the redirect URI for OAuth2 flow.
    add_scope(scope)
        Add an OAuth2 scope to the generator.
    add_scope_calendar()
        Add the Google Calendar scope to the generator.
    build()
        Build and return a GoogleOAuthGenerator instance.

    """
    def __init__(self):
        """
        Initialize the GoogleOAuthBuilder.
        """
        self.manager: GoogleOAuthGenerator = GoogleOAuthGenerator()

    def set_client_secret_path(self, path: str):
        """
        Set the client secret file path.

        Parameters
        ----------
        path : str
            Path to the client secret JSON file.

        Returns
        -------
        GoogleOAuthBuilder
            This instance for method chaining.

        """
        self.manager.client_secret_path = path
        return self

    def set_redirect_uri(self, url: str):
        """
        Set the redirect URI for OAuth2 flow.

        Parameters
        ----------
        url : str
            Redirect URI.

        Returns
        -------
        GoogleOAuthBuilder
            This instance for method chaining.

        """
        self.manager.redirect_uri = url
        return self

    def add_scope(self, scope: str):
        """
        Add an OAuth2 scope to the generator.

        Parameters
        ----------
        scope : str
            OAuth2 scope to add.

        Returns
        -------
        GoogleOAuthBuilder
            This instance for method chaining.

        """
        self.manager.scopes.append(scope)
        return self

    def add_scope_calendar(self):
        """
        Add the Google Calendar scope to the generator.

        Returns
        -------
        GoogleOAuthBuilder
            This instance for method chaining.

        """
        self.manager.scopes.append('https://www.googleapis.com/auth/calendar')
        return self

    def build(self):
        """
        Build and return a GoogleOAuthGenerator instance.

        Returns
        -------
        GoogleOAuthGenerator
            Generated GoogleOAuthGenerator instance.

        """
        return self.manager
