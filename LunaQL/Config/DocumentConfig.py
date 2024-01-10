from typing import Dict

class DocumentConfig:
    def __init__(self, endpoint: str, token: str, type: str, data: Dict):
        """
        Initialize database configuration.
        """
        self.__endpoint = endpoint
        self.__token = token
        self.__type = type
        self.__data = data

    def get_endpoint(self) -> str:
        """
        Get endpoint.
        """

        return self.__endpoint

    def get_token(self) -> str:
        """
        Get token.
        """

        return self.__token

    def get_type(self) -> str:
        """
        Get type.
        """

        return self.__type

    def get_data(self) -> Dict:
        """
        Get data.
        """

        return self.__data
