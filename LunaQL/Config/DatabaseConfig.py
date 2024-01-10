from typing import NamedTuple

class DatabaseConfig:
    def __init__(self, endpoint: str, token: str):
        """
        Initialize database configuration.
        """
        self.__endpoint = endpoint
        self.__token = token

    def get_endpoint(self):
        """
        Get endpoint.
        """

        return self.__endpoint

    def get_token(self):
        """
        Get token.
        """

        return self.__token

