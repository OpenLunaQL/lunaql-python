from typing import List
from typing import Callable
from ..Config.RelationshipConfig import RelationshipConfig

class RelationshipBuilder:
    def __init__(self, config: RelationshipConfig):
        self.__builder = {  "query": { } }
        self.__config = config

        self.__builder["query"].setdefault(config.get_type(), {})
        self.__builder["query"][config.get_type()].setdefault(config.get_collection(), {})

    def select(self, fields: List[str]):
        """
        Create a new query builder.
        """

        return self.__update_query("select", fields)

    def hidden(self, fields: List[str]):
        """
        Hide fields from the collection.
        """

        return self.__update_query('hidden', fields)

    def where(self, field: str, operator: str, value: any):
        """
        Filter the collection.
        """

        return self.__update_query('where', [ field, operator, value ], True)

    def or_where(self, field: str, operator: str, value: any):
        """
        Filter the collection.
        """

        return self.__update_query('orWhere', [ field, operator, value ], True)

    def order_by(self, field: str, direction: str):
        """
        Order the collection.
        """

        return self.__update_query('orderBy').sort(field, direction)

    def sort(self, direction: str):
        """
        Sort the collection.
        """

        return self.__update_query('sort', direction)

    def group_by(self, field: List[str]):
        """
        Group the collection.
        """

        return self.__update_query('groupBy', field)

    def having(self, field: str, operator: str, value: any):
        """
        Filter the collection.
        """

        return self.__update_query('having', [ field, operator, value ])

    def limit(self, limit: int):
        """
        Limit the collection.
        """

        return self.__update_query('limit', limit)

    def skip(self, skip: int):
        """
        Skip documents in the collection.
        """

        return self.__update_query('skip', skip)

    def has_many(self, collection: str, callback: Callable):
        """
        Join collection to another collection.
        """

        # Callable[[RelationshipBuilder]]

        builder = RelationshipBuilder(RelationshipConfig(
            collection=collection,
            type='hasMany'
        ))

        callback(builder)

        if self.__builder["query"][self.__config.get_type()][self.__config.get_collection()].get('hasMany') is None:
            self.__builder["query"][self.__config.get_type()][self.__config.get_collection()].setdefault('hasMany', {})

        self.__builder["query"][self.__config.get_type()][self.__config.get_collection()]['hasMany'][collection] = builder.get_query()['query']['hasMany'][collection]

        return self

    def belongs_to(self, collection: str, callback: Callable):
        """
        Join collection to another collection.
        """

        # Callable[[RelationshipBuilder]]

        builder = RelationshipBuilder(RelationshipConfig(
            collection=collection,
            type='belongsTo'
        ))

        callback(builder)

        if self.__builder["query"][self.__config.get_type()][self.__config.get_collection()].get('belongsTo') is None:
            self.__builder["query"][self.__config.get_type()][self.__config.get_collection()].setdefault('belongsTo', {})

        self.__builder["query"][self.__config.get_type()][self.__config.get_collection()]['belongsTo'][collection] = builder.get_query()['query']['belongsTo'][collection]

        return self

    def get_query(self):
        """
        Get raw query.
        """

        return self.__builder

    def __update_query(self, keys: List[str] | str, query: any, push: bool = False):
        """
        Update query.
        """

        if isinstance(keys, str):
            keys = [ keys ]

        current_node = self.__builder["query"][self.__config.get_type()][self.__config.get_collection()]

        for key in keys[:-1]:
            current_node = current_node.setdefault(key, {})

        last_key = keys[-1]

        if last_key not in current_node:
            current_node[last_key] = [] if push else {}

        if push:
            current_node[last_key].append(query)
        else:
            current_node[last_key] = query

        return self