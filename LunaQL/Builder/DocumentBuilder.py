import requests
from ..Config.DocumentConfig import DocumentConfig

class DocumentBuilder:
    def __init__(self, config: DocumentConfig):
        """
        Create a new document builder.
        """
        self.__config = config

    def into(self, collection: str):
        """
        Insert data into the collection.
        """
        endpoint = f"{self.__config.get_endpoint()}/{collection}"

        if self.__config.get_type() == 'documents':
            endpoint = f"{endpoint}/batch"

        response = requests.put(endpoint, json=self.__config.get_data(), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.__config.get_token()}'
        })

        return response.json()
