from typing import NamedTuple

class RelationshipConfig:
    def __init__(self, collection: str, type: str):
        """
        Initialize database configuration.
        """
        self.__collection = collection
        self.__type = type

    def get_collection(self):
        """
        Get collection.
        """

        return self.__collection

    def get_type(self):
        """
        Get type.
        """

        return self.__type

