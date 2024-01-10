from .QueryBuilder import QueryBuilder
from ..Config.DatabaseConfig import DatabaseConfig

class CollectionBuilder:
    def __init__(self, config: DatabaseConfig):
        """
        Initialize collection builder.
        """

        self.__config = config

    def from_collection(self, collection: str):
        """
        Query from collection.
        """

        return QueryBuilder(self.__config, collection)
