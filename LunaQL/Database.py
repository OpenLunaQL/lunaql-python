from typing import Dict
from .Builder.CollectionBuilder import CollectionBuilder
from .Builder.DocumentBuilder import DocumentBuilder
from .Config.DatabaseConfig import DatabaseConfig
from .Config.DocumentConfig import DocumentConfig

class Database:
    def __init__(self, config: DatabaseConfig):
        """
        Initialize database.

        Parameters:
        - config: DatabaseConfig
        """

        self.__config = config
        self.__collection_builder = CollectionBuilder(config)

    def query(self):
        """
        Query database.
        """

        return self.__collection_builder

    def insert(self, data: Dict, options: Dict = {}):
        """
        Insert new document.
        """
        if isinstance(data, list):
            raise Exception('You can only insert one document.')

        return DocumentBuilder(DocumentConfig(
            endpoint=self.__config.get_endpoint(),
            token=self.__config.get_token(),
            type='document',
            data={
                'data': data,
                'options': options
            }
        ))

    def insertMany(self, data: Dict, options: Dict = {}):
        """
        Insert new documents.
        """
        if not isinstance(data, list):
            raise Exception('You can only insert multiple documents.')

        return DocumentBuilder(DocumentConfig(
            endpoint=self.__config.get_endpoint(),
            token=self.__config.get_token(),
            type='documents',
            data={
                'data': data,
                'options': options
            }
        ))
