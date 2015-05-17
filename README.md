**NOTE:**

This library will not be actively maintained any further. You probably want to see the [RESTArt][1] library (still in development), which is a replacement with better intentions.

---


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


Features
--------

+ Full range of CRUD operations
+ JSON all the time
+ Easy and Extensible Data Validation
+ Intelligent and Extensible Serializer
+ Filtering
+ Pagination
+ Sorting
+ Fields Selection
+ Authentication
+ Sub Resources
+ Cross Origin
+ Support MongoDB
+ Support RDBMS
+ Support Flask
+ Support Django


Documentation
-------------

Complete documentation is available [here][2].


License
-------

[MIT][3]


[1]: https://github.com/RussellLuo/restart
[2]: https://github.com/RussellLuo/resource/blob/master/docs/index.md
[3]: http://opensource.org/licenses/MIT
