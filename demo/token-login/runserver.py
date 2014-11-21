#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['RESOURCE_SETTINGS_MODULE'] = 'settings'

from flask import Flask

from rsrc import settings, Resource, BasicAuth
from rsrc.contrib.root import Root
from rsrc.contrib.db.mongo import Collection, serializer
from rsrc.contrib.token import TokenAuth, TokenView
from rsrc.framework.flask import add_resource, make_root


db = settings.DB


class NoAuth(BasicAuth):
    def authenticated(self, method, auth_params):
        return True


class AllowPOSTAuth(TokenAuth):
    """Subclass `TokenAuth` to allow POST specially.

    In general, `TokenAuth` is enough.
    """
    def authenticated(self, method, auth_params):
        # allow POST in any case
        # e.g.
        #     1. everyone can "POST /users/" to register an account
        #     2. everyone can "POST /tokens/" to login
        if method == 'POST':
            return True
        return super(AllowPOSTAuth, self).authenticated(method, auth_params)


resources = [
    Resource('tokens', TokenView, auth_cls=AllowPOSTAuth),
    Resource('users', Collection, serializer=serializer,
             auth_cls=AllowPOSTAuth,
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
