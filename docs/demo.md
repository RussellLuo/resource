Demo & Test
===========

There are some demos and tests you can try out to explore `Resource`.


Run Demo
--------

### 1. setup environment

    $ cd resource
    $ virtualenv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt

Additional requirements for Django demos

    (env)$ pip install Django

Additional requirements for Flask demos

    (env)$ pip install Flask

### 2. run demo server

#### django-mongodb

    (env)$ cd demo/django-mongodb
    (env)$ export PYTHONPATH=.:../..
    (env)$ # start mongodb server (e.g. sudo mongod)
    (env)$ python manage.py runserver 5000

#### flask-dbviewer

    (env)$ export PYTHONPATH=.
    (env)$ # start mongodb server (e.g. sudo mongod)
    (env)$ python dbviewer.py mongodb://localhost:27017 test

#### flask-mongodb

    (env)$ export PYTHONPATH=.
    (env)$ # start mongodb server (e.g. sudo mongod)
    (env)$ python demo/flask-mongodb/runserver.py

#### flask-sqlite

    (env)$ export PYTHONPATH=.
    (env)$ python demo/flask-sqlite/create_tables.py
    (env)$ python demo/flask-sqlite/runserver.py

#### token-login

    (env)$ cd demo/token-login
    (env)$ export PYTHONPATH=.:../..
    (env)$ # start mongodb server (e.g. sudo mongod)
    (env)$ python runserver.py

#### dufilter

    (env)$ cd demo/dufilter
    (env)$ export PYTHONPATH=.:../..
    (env)$ # start mongodb server (e.g. sudo mongod)
    (env)$ python runserver.py


Run Test
--------

### Test Mongo

    (env)$ # Run django-mongodb or flask-mongodb demo

    (env)$ # Run Test
    (env)$ python tests/test_mongo.py

### Test Sqla

    (env)$ # Run flask-sqlite demo

    (env)$ # Run Test
    (env)$ python tests/test_sqla.py

### Test Token

    (env)$ # Run token-login demo

    (env)$ # Run Test
    (env)$ python tests/test_token.py

### Test DuFilter

    (env)$ # Run dufilter demo

    (env)$ # Run Test
    (env)$ python tests/test_dufilter.py
