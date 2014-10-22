#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from pymongo import MongoClient
from flask import Flask

from resource import Resource, Form, Filter, BasicAuth
from resource.root import Root
from resource.contrib.db.mongo import Collection, MongoSerializer
from resource.contrib.framework.flask import add_resource, make_root


DB = MongoClient().test


class UserAuth(BasicAuth):
    def authenticated(self, auth_params):
        return True


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


resources = [
    Resource('users', Collection, form_cls=UserForm,
             serializer_cls=MongoSerializer, filter_cls=UserFilter,
             auth_cls=UserAuth, kwargs={'db': DB, 'table_name': 'user'})
]


app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)

    root = Resource('root', Root, uri='/', auth_cls=UserAuth,
                    kwargs={'resources': resources})
    make_root(app, root)

    app.run(debug=True)
