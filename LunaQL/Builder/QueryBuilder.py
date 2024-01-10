import requests
from typing import Callable, List, Dict
from .RelationshipBuilder import RelationshipBuilder
from ..Config.RelationshipConfig import RelationshipConfig

class QueryBuilder:
    def __init__(self, config, collection: str):
        self.__builder = { "query": { "from": { } } }
        self.__config = config
        self.__collection = collection

        self.__builder["query"]["from"].setdefault(collection, {})

    def select(self, fields: List[str]):
        """
        Create a new query builder.
        """

        return self.__update_query('select', fields)

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

        self.__update_query('orderBy', field)
        self.__update_query('sort', direction)

        return self

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

    def has_many(self, collection: str, callback: Callable[[RelationshipBuilder], RelationshipBuilder]):
        """
        Join collection to another collection.
        """

        # Callable[[RelationshipBuilder]]

        builder = RelationshipBuilder(RelationshipConfig(
            collection=collection,
            type='hasMany'
        ))

        callback(builder)

        if self.__builder["query"]["from"][self.__collection].get('hasMany') is None:
            self.__builder["query"]["from"][self.__collection]['hasMany'] = { }

        self.__builder["query"]["from"][self.__collection]['hasMany'][collection] = builder.get_query()['query']['hasMany'][collection]

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

        if self.__builder["query"]["from"][self.__collection].get('belongsTo') is None:
            self.__builder["query"]["from"][self.__collection]['belongsTo'] = { }

        self.__builder["query"]["from"][self.__collection]['belongsTo'][collection] = builder.get_query()['query']['belongsTo'][collection]

        return self

    def update(self, data: dict) -> int:
        """
        Update documents in the collection.
        """

        self.__update_query('do', 'update')
        self.__update_query('set', data)

        return self.__persist()['affected']

    def delete(self) -> int:
        """
        Delete documents in the collection.
        """

        self.__update_query('do', 'delete')

        return self.__persist()['affected']

    def count(self) -> int:
        """
        Count documents in the collection.
        """

        self.__update_query('do', 'count')

        return self.__persist()['count']

    def exists(self) -> bool:
        """
        Check if documents exist in the collection.
        """

        self.__update_query('do', 'exists')

        return self.__persist()['exists']

    def list(self, property: str = None) -> List[ str | int ]:
        """
        Pluck a property from the collection.
        """

        self.__update_query('do', 'list')

        if property:
            self.__update_query('listBy', property)

        return self.__persist()

    def fetch(self) -> List[Dict]:
        """
        Fetch documents from the collection.
        """

        self.__update_query('do', 'fetch')

        return self.__persist()

    def fetch_first(self) -> Dict:
        """
        Fetch the first document from the collection.
        """

        self.__update_query('do', 'fetchFirst')

        return self.__persist()

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

        current_node = self.__builder["query"]["from"][self.__collection]

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

    def __persist(self):
        """
        Persist query.
        """

        response = requests.post(self.__config.get_endpoint(), json=self.get_query(), headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.__config.get_token()}'
        })

        return response.json()[self.__collection]
