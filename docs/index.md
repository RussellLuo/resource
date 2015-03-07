Resource
========

A Python library concentrated on the Resource layer of RESTful APIs.


Philosophy
----------

You have data somewhere:

1. physical data stored in databases like MongoDB (NoSQL) or MySQL (RDBMS)
2. virtual data existing in applications (e.g. data in business logic)

and you want to expose it to your users through a RESTful Web API. `Resource` is a convenient library that allows you to do so.

`Resource` is database agnostic and web framework agnostic, which means you should/can choose databases (MongoDB, MySQL, etc.) and web frameworks (Flask, Django, etc.) yourself.


Installation
------------

Install `Resource` with `pip`:

    $ pip install Resource

Install development version from `GitHub`:

    $ git clone https://github.com/RussellLuo/resource.git
    $ cd resource
    $ python setup.py install


Quickstart
----------

+ [Todo](quickstart.md#todo)
+ [HTTP-verb and View-method](quickstart.md#http-verb-and-view-method)


Features
--------

+ [Full range of CRUD operations](features.md#full-range-of-crud-operations)
+ [JSON all the time](features.md#json-all-the-time)
+ [Easy and Extensible Data Validation](features.md#easy-and-extensible-data-validation)
+ [Intelligent and Extensible Serializer](features.md#intelligent-and-extensible-serializer)
+ [Filtering](features.md#filtering)
+ [Pagination](features.md#pagination)
+ [Sorting](features.md#sorting)
+ [Fields Selection](features.md#fields-selection)
+ [Authentication](features.md#authentication)
+ [Sub Resources](features.md#sub-resources)
+ [Cross Origin](features.md#cross-origin)
+ [Support MongoDB](features.md#support-mongodb)
+ [Support RDBMS](features.md#support-rdbms)
+ [Support Flask](features.md#support-flask)
+ [Support Django](features.md#support-django)


Demo & Test
-----------

+ [Run Demo](demo.md#run-demo)
+ [Run Test](demo.md#run-test)
