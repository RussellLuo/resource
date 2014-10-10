#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from jsonform import JsonForm
from pymongo import MongoClient
from flask import Flask

from resource import Resource
from resource.index import Index
from resource.db.mongo import Collection, MongoSerializer
from resource.contrib.framework.flask import add_resource, make_index


DB = MongoClient().test


class UserForm(JsonForm):
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


resources = [
    Resource('users', Collection, form=UserForm,
             serializer=MongoSerializer,
             kwargs={'db': DB, 'table_name': 'user'})
]


app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)

    index = Resource('index', Index, uri='/',
                     kwargs={'resources': resources})
    make_index(app, index)

    app.run(debug=True)
