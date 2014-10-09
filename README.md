Resource
========

A library concentrated on the Resource layer of RESTful API.


Philosophy
----------

You have data somewhere:

1. physical data stored in databases like MongoDB (NoSQL) or MySQL (RDBMS)
2. virtual data existed in applications

and you want to expose it to your users through a RESTful Web API. `Resource` is a convenient library that allows you to do so.

`Resource` is database agnostic and web framework agnostic, which means you should/can choose databases (MongoDB, MySQL, etc.) and web frameworks (Flask, Django, etc.) yourself.


Features
--------

+ Full range of CRUD operations
+ JSON all the time
+ Easy and Extensible Data Validation for POST/PUT/PATCH
+ Intelligent and Extensible Serializer
+ Filtering
+ Pagination
+ Sorting
+ Fields Selection
+ Support MongoDB
+ Support RDBMS (SQLite, MySQL, etc.)
+ Support Flask


Roadmap
-------

+ Enhance Filtering
+ Use [automap][2] instead of [SQLSoup][3] (which is obsolete)
+ Authentication
+ HATEOAS
+ Documentation
+ Support Django


Run REST Server
---------------

### 1. setup environment

    $ cd resource
    $ virtualenv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt

### 2. configure resources in your `settings.py`

    from pymongo import MongoClient
    from jsonform import JsonForm

    from resource import Resource
    from resource.db.mongo import Collection, MongoSerializer

    DB = MongoClient().test

    class UserForm(JsonForm):
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'password': {'type': 'string'}
            }
        }

    resources = [
        Resource('users', Collection, form=UserForm,
                serializer=MongoSerializer,
                kwargs={'engine': DB['user']})
    ]

### 3. run demo server

    (env)$ # Set PYTHONPATH
    (env)$ export PYTHONPATH=.

    (env)$ # Run MongoDB demo
    (env)$ # start mongodb server (e.g. sudo mongod)
    (env)$ python demo/mongodb/settings.py

    (env)$ # Run SQLite demo
    (env)$ python demo/sqlite/create_tables.py
    (env)$ python demo/sqlite/settings.py

Use REST Client
---------------

### GET

#### 1. Get a list of items

    $ curl -i http://127.0.0.1:5000/users/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:53:01 GMT

    []

#### 2. Filtering

    $ curl -i http://127.0.0.1:5000/users/?name=XX

#### 3. Get a single item

    $ curl -i http://127.0.0.1:5000/users/<pk>/

### POST

    $ curl -i -H "Content-Type: application/json" -d '{"name": "russell"}' http://127.0.0.1:5000/users/
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:55:37 GMT

    ""
    $ curl http://127.0.0.1:5000/users/
    [{"_id": "541fb9d91d41c81a78f2dca4", "name": "russell"}]

### PUT

    $ curl -i -X PUT -H "Content-Type: application/json" -d '{"name": "tracey"}' http://127.0.0.1:5000/users/541fb9d91d41c81a78f2dca4/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:58:45 GMT

    $ curl http://127.0.0.1:5000/users/
    [{"_id": "541fb9d91d41c81a78f2dca4", "name": "tracey"}]

### PATCH

Please refer to [RFC 6902][1] for the exact `JSON Patch` syntax.

    $ curl -i -X PATCH -H "Content-Type: application/json" -d '[{"op": "add", "path": "/password", "value": "123456"}]' http://127.0.0.1:5000/users/541fb9d91d41c81a78f2dca4/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 06:06:44 GMT

    $ curl http://127.0.0.1:5000/users/
    [{"password": "123456", "name": "tracey", "_id": "541fb9d91d41c81a78f2dca4"}]

### DELETE

    $ curl -i -X DELETE http://127.0.0.1:5000/users/541fb9d91d41c81a78f2dca4/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 06:08:58 GMT

    $ curl http://127.0.0.1:5000/users/
    []


Run Test
--------

### Test Mongo

    (env)$ # Run MongoDB demo

    (env)$ # Run Test
    (env)$ python tests/test_mongo.py

### Test Sqla

    (env)$ # Run SQLite demo

    (env)$ # Run Test
    (env)$ python tests/test_sqla.py

**BTW**: For REST Client of `requests` version, see `tests`.


[1]: http://tools.ietf.org/html/rfc6902
[2]: http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html
[3]: https://sqlsoup.readthedocs.org/en/latest/index.html
