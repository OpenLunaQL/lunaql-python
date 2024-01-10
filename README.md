# LunaQL Python Client

This is a Python client for the [LunaQL](https://lunaql.com) NoSQL database.

## Example

```python
from LunaQL.Database import Database
from LunaQL.Config.DatabaseConfig import DatabaseConfig

db = Database(DatabaseConfig(
    endpoint="<endpoint>",
    token="<token>"
))

object_ids = (
    db.query()
        .from_collection('users')
        .limit(1)
        .select(['_fk'])
        .list('_fk')
)

results = (
    db.query()
        .from_collection('users')
        .where('_fk', 'in', object_ids)
        .has_many('tasks', lambda q: q.where('user_id', '=', '$._id').order_by('created_at', 'asc'))
        .fetch()
)

print(results)
```

## Todo
- [ ] Add tests
- [ ] Implement error handling
- [ ] Implement more query methods

Security
-------

If you discover any security related issues, please email donaldpakkies@gmail.com instead of using the issue tracker.

License
-------

The MIT License (MIT). Please see [License File](LICENSE) for more information.

