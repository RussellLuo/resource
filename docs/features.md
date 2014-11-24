Features
========

Below is a list of main features that any Resource-based APIs can expose.


Full range of CRUD operations
-----------------------------

APIs can support the full range of [CRUD][1] operations. The following table shows Resource’s implementation of CRUD via REST:

Action  | HTTP Verb | Context
------- | --------- | ---------
Create  | POST      | List
Read    | GET       | List/Item
Update  | PATCH     | Item
Replace | PUT       | Item
Delete  | DELETE    | Item

### POST

    $ curl -i -H "Content-Type: application/json" -d '{"name": "russell", "password": "123456", "date_joined": "datetime(2014-10-11T00:00:00Z)"}' http://127.0.0.1:5000/users/
    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 35
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Sat, 11 Oct 2014 13:45:11 GMT

    {"_id": "543934671d41c812802711f3"}

### GET

Get a list of items.

    $ curl -i http://127.0.0.1:5000/users/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:53:01 GMT

    [{"password": "123456", "date_joined": "2014-10-11T00:00:00Z", "name": "russell", "_id": "543934671d41c812802711f3"}]

Get a single item.

    $ curl -i http://127.0.0.1:5000/users/543934671d41c812802711f3/
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 2
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Mon, 22 Sep 2014 05:53:01 GMT

    {"password": "123456", "date_joined": "2014-10-11T00:00:00Z", "name": "russell", "_id": "543934671d41c812802711f3"}

### PATCH

Please refer to [RFC 6902][2] for the exact `JSON Patch` syntax.

    $ curl -i -X PATCH -H "Content-Type: application/json" -d '[{"op": "add", "path": "/password", "value": "666666"}]' http://127.0.0.1:5000/users/543934671d41c812802711f3/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Sat, 11 Oct 2014 13:59:26 GMT

### PUT

    $ curl -i -X PUT -H "Content-Type: application/json" -d '{"name": "tracey", "password": "123456", "date_joined": "datetime(2014-10-11T00:00:00Z)"}' http://127.0.0.1:5000/users/543934671d41c812802711f3/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Sat, 11 Oct 2014 13:49:00 GMT

### DELETE

    $ curl -i -X DELETE http://127.0.0.1:5000/users/543934671d41c812802711f3/
    HTTP/1.0 204 NO CONTENT
    Content-Type: application/json
    Content-Length: 0
    Server: Werkzeug/0.9.6 Python/2.7.3
    Date: Sat, 11 Oct 2014 14:02:00 GMT


JSON all the time
-----------------

All request/response data over the wire is in JSON-format.


Easy and Extensible Data Validation
-----------------------------------

Please refer to [JsonForm][3] for exact validation schema.

    from resource import Form

    class UserForm(Form):
        def validate_datetime(value):
            if not isinstance(value, datetime):
                return 'value must be an instance of `datetime`'

        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'password': {'type': 'string'},
                'date_joined': {'custom': validate_datetime}
            }
        }


Intelligent and Extensible Serializer
-------------------------------------

Please refer to [JsonSir][4] for serialization details.

### Deserialize Schema

Convert request data (in JSON/Query-Parameter) to Python type:

Value in JSON/Query-Parameter        | Value in Python
------------------------------------ | -----------------------------------------
"int(10)"                            | 10
"bool(true)"                         | True
"string"                             | "string"
"regex(/russ/)"                      | re._pattern_type
"objectid(543934671d41c812802711f3)" | bson.ObjectId("543934671d41c812802711f3")
"datetime(2014-10-11T00:00:00Z)"     | datetime.datetime(2014, 10, 11)

If you set `DATE_FORMAT` to "%Y-%m-%d %H:%M:%S", then:

    "datetime(2014-10-11 00:00:00)" => datetime.datetime(2014, 10, 11)

### Serialize Schema

Convert response data (in Python) to JSON:

Value in Python                           | Value in JSON              | Value in JSON (`WITH_TYPE_NAME` == True)
----------------------------------------- | -------------------------- | --------------------------
10                                        | 10                         | 10
True                                      | true                       | true
"string"                                  | "string"                   | "string"
re._pattern_type                          | "/russ/"                   | "regex(/russ/)"
bson.ObjectId("543934671d41c812802711f3") | "543934671d41c812802711f3" | "objectid(543934671d41c812802711f3)"
datetime.datetime(2014, 10, 11)           | "2014-10-11T00:00:00Z"     | "datetime(2014-10-11T00:00:00Z)"

If you set `DATE_FORMAT` to "%Y-%m-%d %H:%M:%S", then:

    datetime.datetime(2014, 10, 11) => "2014-10-11 00:00:00" => "datetime(2014-10-11 00:00:00)"


Filtering
---------

With a single condition:

    $ curl http://127.0.0.1:5000/users/543934671d41c812802711f3/?name=russell

With multiple conditions in AND mode:

    $ curl http://127.0.0.1:5000/users/543934671d41c812802711f3/?name=russell&date_joined=datetime(2014-10-11T00:00:00Z)

By subclassing `Filter` class, you can do more complex filtering:

    from resource import Filter

    class UserFilter(Filter):
        def query_date_range(self, query_params):
            date_joined_gt = query_params.pop('date_joined_gt', None)
            date_joined_lt = query_params.pop('date_joined_lt', None)

            conditions = {}

            if date_joined_gt:
                conditions.update({'$gt': date_joined_gt})

            if date_joined_lt:
                conditions.update({'$lt': date_joined_lt})

            if conditions:
                return {'date_joined': conditions}
            else:
                return {}

Then, you can filter users with `date_joined_gt` and `date_joined_lt` like this:

    $ curl http://127.0.0.1:5000/users/?date_joined_gt=datetime(2014-10-01T00:00:00Z)&date_joined_lt=datetime(2014-10-03T00:00:00Z)


### DuFilter

`Resource` is shipped with a class `DuFilter`, which supports double-underscore style filtering.

With the help of `DuFilter`, you can filter resources like this (without any extra code):

    $ curl http://127.0.0.1:5000/users/?username__in=russell&username__in=tracey
    $ curl http://127.0.0.1:5000/users/?date_joined__gt=datetime(2014-10-01T00:00:00Z)&date_joined__lt=datetime(2014-10-03T00:00:00Z)

Below is the full list of Comparison Operators that `DuFilter` supports:

Comparison Operators | Meaning               | Example
-------------------- | --------------------- | -----------------------------------------------
ne                   | not equal             | username__ne=russell
lt                   | less than             | date_joined__lt=datetime(2014-10-01T00:00:00Z)
lte                  | less than or equal    | date_joined__lte=datetime(2014-10-01T00:00:00Z)
gt                   | greater than          | date_joined__gt=datetime(2014-10-01T00:00:00Z)
gte                  | greater than or equal | date_joined__gte=datetime(2014-10-01T00:00:00Z)
in                   | within range          | `username__in`=russell&`username__in`=tracey
like                 | regex match           | username__like=^russ


Pagination
----------

You can paginate items with the following two keywords in query parameter:

Keyword  | Default
-------- | -------
page     | 1
per_page | 20

You may want to specify `page` and `per_page` explicitly.

    $ curl http://127.0.0.1:5000/users/?page=2&per_page=10


Sorting
-------

You can sort items with the keyword `sort` in query parameter:

Sign       | Order
---------- | ----------
+ or empty | Ascending
-          | Descending

For example, you can sort users first by `name` in ascending-order and second by `age` in descending-order:

    $ curl http://127.0.0.1:5000/users/?sort=name,-age


Fields Selection
----------------

You can select/limit returned fields of each item with the keyword `fields` in query parameter.

For example, the following request will receive all users with only `name` and `password` fields in each user:

    $ curl http://127.0.0.1:5000/users/?fields=name,password


Authentication
--------------

### Basic Authentication

#### 1. No authentication

    from resource import BasicAuth

    class NoAuth(BasicAuth):
        def authenticated(self, method, auth_params):
            return True

For resources protected by `NoAuth`, you can access them without credentials:

    $ curl http://127.0.0.1:5000/<resource>/

#### 2. Simple authentication

    from resource import BasicAuth

    class SimpleAuth(BasicAuth):
        def authenticated(self, method, auth_params):
            username = auth_params.get('username')
            password = auth_params.get('password')
            return (username == 'russell' and password == '123456')

For resources protected by `SimpleAuth`, you must set `Authorization` header to access them:

    $ curl -u russell:encrypted http://127.0.0.1:5000/<resource>/

#### 3. Complex authentication

    from resource import BasicAuth

    class ComplexAuth(BasicAuth):
        def authenticated(self, method, auth_params):
            # allow GET in any case
            if method == 'GET':
                return True
            # lookup in the database
            username = auth_params.get('username')
            password = auth_params.get('password')
            user = db.user.find_one({'username': username, 'password': password})
            return bool(user)

For resources protected by `ComplexAuth`, you can access them via `GET` without credentials:

    $ curl http://127.0.0.1:5000/<resource>/

But you must give credentials of a registered user to access these resources via other HTTP methods (i.e. `POST`, `PUT`, `PATCH`, `DELETE`):

    $ curl -u russell:encrypted -X DELETE http://127.0.0.1:5000/<resource>/<pk>

### Token-based Authentication

`Resource` also support Token-based authentication.

#### 1. At server side

First, you must subclass `TokenUser`:

    from bson import ObjectId
    from resource.contrib.token import TokenUser

    class MongoTokenUser(TokenUser):
        @classmethod
        def get_key(self, username, password):
            user = db.user.find_one({'username': username, 'password': password})
            if not user:
                return None, None

            return str(user['_id']), user['jwt_secret']

        @classmethod
        def exists(self, pk, secret):
            if pk is None or secret is None:
                return False
            user = db.user.find_one({'_id': ObjectId(pk), 'jwt_secret': secret})
            return bool(user)

        @classmethod
        def invalidate_key(cls, pk):
            try:
                pk = ObjectId(pk)
            except:
                return False

            new_secret = str(uuid.uuid4())
            res = db.user.update(
                {'_id': pk},
                {'$set': {'jwt_secret': new_secret}}
            )
            return res['updatedExisting']

Next, set class `MongoTokenUser` (with its module-path) as the value of `TOKEN_USER` in settings:

    TOKEN_USER = '<module_path>.MongoTokenUser'

#### 2. At client side

Then, you can get a token and use it by following the steps below:

1. POST (with username and password) to generate a token

        $ curl -X POST -H "Content-Type: application/json" -d '{"username":"russell","password":"123456"}' http://127.0.0.1:5000/tokens/

2. get the token from the response (in JSON format) of POST

        $ {"id": "543934671d41c812802711f3", "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQxNDIyNDExOSwiaWF0IjoxNDE0MjIwNTE5fQ.eyJwayI6IjU0NGI0YWRhMWQ0MWM4MzExMjRhNDBjZCJ9.d_6Oi4ePS7z9NhK9b9J23H3KQx4u_EdzT-VHDnV2fC8", "expires": 3600}

3. set the token as username part in the Authorization header to access resources

        $ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQxNDIyNDExOSwiaWF0IjoxNDE0MjIwNTE5fQ.eyJwayI6IjU0NGI0YWRhMWQ0MWM4MzExMjRhNDBjZCJ9.d_6Oi4ePS7z9NhK9b9J23H3KQx4u_EdzT-VHDnV2fC8:unused http://127.0.0.1:5000/<resource>/


Support MongoDB
---------------

See [Demo & Test](demo.md).


Support RDBMS
-------------

`Resource` supports all RDBMS supported by `SQLAlchemy`. As of this writing, that includes:

+ MySQL (MariaDB)
+ PostgreSQL
+ SQLite
+ Oracle
+ Microsoft SQL Server
+ Firebird
+ Drizzle
+ Sybase
+ IBM DB2
+ SAP Sybase SQL Anywhere
+ MonetDB

See [Demo & Test](demo.md).


Support Flask
-------------

See [Demo & Test](demo.md).


Support Django
--------------

See [Demo & Test](demo.md).


[1]: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[2]: http://tools.ietf.org/html/rfc6902
[3]: https://github.com/RussellLuo/jsonform
[4]: https://github.com/RussellLuo/jsonsir
