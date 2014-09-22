Resource
========

A library concentrated on the Resource layer of RESTful API.


Philosophy
----------

You have data somewhere:

1. actual data stored in databases like MongoDB (NoSQL) or MySQL (RDBMS)
2. virtual data existed in applications

and you want to expose it to your users through a RESTful Web API. `Resource` is a convenient library that allows you to do so.

`Resource` is database agnostic and web framework agnostic, which means you can choose database (MongoDB, MySQL, etc.) and web framework (flask, Django, etc.) yourself.


Getting Started
---------------

### Run REST Server

#### setup environment

    $ cd resource
    $ virtualenv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt

#### configure resources in your `settings.py`

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

3. run demo server

    (env)$ python demo/settings.py

### Use REST Client

#### GET

    $ curl -i http://127.0.0.1:5000/users/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:53:01 GMT

    []

#### POST

    $ curl -i -H "Content-Type: application/json" -d '{"name": "russell"}' http://127.0.0.1:5000/users/
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:55:37 GMT

    ""
    $ curl http://127.0.0.1:5000/users/
    [{"_id": "541fb9d91d41c81a78f2dca4", "name": "russell"}]

#### PUT

    $ curl -i -X PUT -H "Content-Type: application/json" -d '{"name": "tracey"}' http://127.0.0.1:5000/users/541fb9d91d41c81a78f2dca4/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:58:45 GMT

    $ curl http://127.0.0.1:5000/users/
    [{"_id": "541fb9d91d41c81a78f2dca4", "name": "tracey"}]

#### PATCH

    $ curl -i -X PATCH -H "Content-Type: application/json" -d '[{"op": "add", "path": "/password", "value": "123456"}]' http://127.0.0.1:5000/users/541fb9d91d41c81a78f2dca4/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 06:06:44 GMT

    $ curl http://127.0.0.1:5000/users/
    [{"password": "123456", "name": "tracey", "_id": "541fb9d91d41c81a78f2dca4"}]

#### DELETE

    $ curl -i -X DELETE http://127.0.0.1:5000/users/541fb9d91d41c81a78f2dca4/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 06:08:58 GMT

    $ curl http://127.0.0.1:5000/users/
    []
