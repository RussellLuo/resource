#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson import ObjectId

from resource import settings, Resource, BasicAuth
from resource.contrib.token import TokenAuth, TokenView


db = settings.DB


class NoAuth(BasicAuth):
    def authenticated(self, method, auth_params):
        return True


class TokenBasedAuth(TokenAuth):
    def has_user(self, user_pk):
        user = db.user.find_one({'_id': ObjectId(user_pk)})
        return bool(user)


class Token(TokenView):
    def get_user_pk(self, username, password):
        user = db.user.find_one({'username': username, 'password': password})
        if not user:
            return None

        return str(user['_id'])


token = Resource('tokens', Token, auth_cls=NoAuth)
