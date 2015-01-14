#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from pymongo import MongoClient

from rsrc import Resource, Form, Filter
from rsrc.contrib.root import Root
from rsrc.contrib.db.mongo import Collection, serializer


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
    Resource('users', Collection, serializer=serializer,
             form_cls=UserForm, filter_cls=UserFilter,
             kwargs={'db': DB, 'table_name': 'user'})
]


root = Resource('root', Root, uri='/',
                kwargs={'resources': resources})
