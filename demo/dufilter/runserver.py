#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from flask import Flask

from rsrc import Resource, BasicAuth
from rsrc.contrib.root import Root
from rsrc.contrib.db.mongo import Collection, MongoSerializer
from rsrc.contrib.dufilter import DuFilter
from rsrc.framework.flask import add_resource, make_root


DB = MongoClient().test


class MyAuth(BasicAuth):
    def authenticated(self, method, auth_params):
        return True


resources = [
    Resource('users', Collection, serializer_cls=MongoSerializer,
             filter_cls=DuFilter, auth_cls=MyAuth,
             kwargs={'db': DB, 'table_name': 'user'})
]


app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)

    root = Resource('root', Root, uri='/', auth_cls=MyAuth,
                    kwargs={'resources': resources})
    make_root(app, root)

    app.run(debug=True)
