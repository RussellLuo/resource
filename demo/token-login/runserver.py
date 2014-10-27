#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['RESOURCE_SETTINGS_MODULE'] = 'settings'

from flask import Flask

from resource import settings, Resource, BasicAuth
from resource.contrib.root import Root
from resource.contrib.db.mongo import Collection, MongoSerializer
from resource.contrib.token import TokenAuth, TokenView
from resource.framework.flask import add_resource, make_root


db = settings.DB


class NoAuth(BasicAuth):
    def authenticated(self, method, auth_params):
        return True


class UserAuth(TokenAuth):
    """Subclass `TokenAuth` to allow POST specially.

    In general, `TokenBasedAuth` is enough.
    """
    def authenticated(self, method, auth_params):
        # everyone can POST to register an account
        if method == 'POST':
            return True
        return super(UserAuth, self).authenticated(method, auth_params)


resources = [
    Resource('tokens', TokenView, auth_cls=NoAuth),
    Resource('users', Collection, auth_cls=UserAuth,
             serializer_cls=MongoSerializer,
             kwargs={'db': settings.DB, 'table_name': 'user'})
]


app = Flask(__name__)


if __name__ == '__main__':
    for r in resources:
        add_resource(app, r)

    root = Resource('root', Root, uri='/', auth_cls=NoAuth,
                    kwargs={'resources': resources})
    make_root(app, root)

    app.run(debug=True)
