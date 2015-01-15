Demo & Test
===========

There are some demos and tests you can try out to explore `Resource`.


Run Demo
--------

### 1. setup environment

    $ cd resource
    $ virtualenv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt

Additional requirements for Django demos

    (venv)$ pip install Django

Additional requirements for Flask demos

    (venv)$ pip install Flask

### 2. run demo server

#### quickstart

    (venv)$ export PYTHONPATH=.
    (venv)$ python demo/quickstart/runserver.py

#### mini-trello

    (venv)$ export PYTHONPATH=.
    (venv)$ python demo/mini-trello/runserver.py

#### django-mongodb

    (venv)$ cd demo/django-mongodb
    (venv)$ export PYTHONPATH=.:../..
    (venv)$ # start mongodb server (e.g. sudo mongod)
    (venv)$ python manage.py runserver 5000

#### flask-dbviewer

    (venv)$ cd demo/flask-dbviewer
    (venv)$ export PYTHONPATH=.:../..
    (venv)$ # start mongodb server (e.g. sudo mongod)
    (venv)$ python runserver.py mongodb://localhost:27017 test

#### flask-mongodb

    (venv)$ export PYTHONPATH=.
    (venv)$ # start mongodb server (e.g. sudo mongod)
    (venv)$ python demo/flask-mongodb/runserver.py

#### flask-sqlite

    (venv)$ export PYTHONPATH=.
    (venv)$ python demo/flask-sqlite/create_tables.py
    (venv)$ python demo/flask-sqlite/runserver.py

#### token-login

    (venv)$ cd demo/token-login
    (venv)$ export PYTHONPATH=.:../..
    (venv)$ # start mongodb server (e.g. sudo mongod)
    (venv)$ python runserver.py

#### dufilter

    (venv)$ export PYTHONPATH=.
    (venv)$ # start mongodb server (e.g. sudo mongod)
    (venv)$ python demo/dufilter/runserver.py


Run Test
--------

### Test Mongo

    (venv)$ # Run django-mongodb or flask-mongodb demo

    (venv)$ # Run Test
    (venv)$ python tests/test_mongo.py

### Test Sqla

    (venv)$ # Run flask-sqlite demo

    (venv)$ # Run Test
    (venv)$ python tests/test_sqla.py

### Test Token

    (venv)$ # Run token-login demo

    (venv)$ # Run Test
    (venv)$ python tests/test_token.py

### Test DuFilter

    (venv)$ # Run dufilter demo

    (venv)$ # Run Test
    (venv)$ python tests/test_dufilter.py
