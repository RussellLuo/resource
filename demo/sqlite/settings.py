#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonform import JsonForm
from sqlalchemy import create_engine
from flask import Flask

from resource import Resource
from resource.db.sqla import Table
from resource.contrib.framework.flask import add_resource


DB = create_engine('sqlite:///sqlite.db')


class UserForm(JsonForm):
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'password': {'type': 'string'}
        }
    }


resources = [
    Resource('users', Table, form=UserForm,
             kwargs={'db': DB, 'table': 'user'})
]


app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)

    app.run(debug=True)
