#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from jsonform import JsonForm
from sqlalchemy import create_engine
from flask import Flask

from resource import Resource
from resource.index import Index
from resource.db.sqla import Table, SqlaSerializer
from resource.contrib.framework.flask import add_resource, make_index


DB = create_engine('sqlite:///sqlite.db')


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
    Resource('users', Table, form=UserForm,
             serializer=SqlaSerializer,
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
