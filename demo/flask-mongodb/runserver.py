#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from pymongo import MongoClient
from flask import Flask

from rsrc import Resource, Form, Filter, query_params
from rsrc.contrib.root import Root
from rsrc.contrib.db.mongo import Collection, serializer
from rsrc.framework.flask import add_resource, make_root


DB = MongoClient().test


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


class UserFilter(Filter):
    @query_params('date_joined_gt', 'date_joined_lt')
    def query_date_range(self, date_joined_gt=None, date_joined_lt=None):
        conditions = {}

        if date_joined_gt:
            conditions.update({'$gt': date_joined_gt})

        if date_joined_lt:
            conditions.update({'$lt': date_joined_lt})

        if conditions:
            return {'date_joined': conditions}
        else:
            return {}


resources = [
    Resource('users', Collection, serializer=serializer,
             form_cls=UserForm, filter_cls=UserFilter,
             kwargs={'db': DB, 'table_name': 'user'})
]


app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)

    root = Resource('root', Root, uri='/',
                    kwargs={'resources': resources})
    make_root(app, root)

    app.run(debug=True)
