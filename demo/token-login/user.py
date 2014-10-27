#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bson import ObjectId

from resource import settings
from resource.contrib.token import TokenUser


db = settings.DB


class MongoTokenUser(TokenUser):

    @classmethod
    def get_key(self, username, password):
        user = db.user.find_one({'username': username, 'password': password})
        if not user:
            return None

        return dict(pk=str(user['_id']), secret=user['jwt_secret'])

    @classmethod
    def exists(self, key):
        pk = key.get('pk')
        secret = key.get('secret')
        if pk is None or secret is None:
            return False
        user = db.user.find_one({'_id': ObjectId(pk), 'jwt_secret': secret})
        return bool(user)
