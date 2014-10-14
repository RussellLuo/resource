#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['RESOURCE_SETTINGS_MODULE'] = 'settings'

import sys

from pymongo import MongoClient
from flask import Flask

from resource import Resource, BasicAuth
from resource.index import Index
from resource.db.mongo import Collection, MongoSerializer
from resource.contrib.framework.flask import add_resource, make_index


app = Flask(__name__)


class TrivialAuth(BasicAuth):

    def authenticated(self, auth_params):
        username = auth_params.get('username')
        password = auth_params.get('password')
        if username and password:
            return True

    def authorized(self):
        return True


def get_resources(db):
    resources = [
        Resource(name, Collection,
                 serializer_cls=MongoSerializer, auth_cls=TrivialAuth,
                 kwargs={'db': db, 'table_name': name})
        for name in db.collection_names()
    ]
    return resources


def register_resources(app, resources):
    for r in resources:
        add_resource(app, r)

    index = Resource('index', Index, uri='/', auth_cls=TrivialAuth,
                     kwargs={'resources': resources})
    make_index(app, index)


if __name__ == '__main__':

    argv = sys.argv
    if len(argv) != 3:
        sys.stdout.write('Usage: python dbserver.py <db_uri> <db_name>\n')
        sys.exit(1)

    # e.g. 'mongodb://localhost:27017'
    db_uri = argv[1]
    # e.g. 'test'
    db_name = argv[2]

    DB = getattr(MongoClient(db_uri), db_name)

    resources = get_resources(DB)
    register_resources(app, resources)

    app.run(host='0.0.0.0', debug=True)
