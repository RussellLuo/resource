#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from bson import ObjectId

from resource import settings
from resource.contrib.token import TokenUser


db = settings.DB


class MongoTokenUser(TokenUser):

    @classmethod
    def get_key(self, username, password):
        user = db.user.find_one({'username': username, 'password': password})
        if not user:
            return None, None

        return str(user['_id']), user['jwt_secret']

    @classmethod
    def exists(self, pk, secret):
        if pk is None or secret is None:
            return False
        user = db.user.find_one({'_id': ObjectId(pk), 'jwt_secret': secret})
        return bool(user)

    @classmethod
    def invalidate_key(cls, pk):
        try:
            pk = ObjectId(pk)
        except:
            return False

        new_secret = str(uuid.uuid4())
        res = db.user.update(
            {'_id': pk},
            {'$set': {'jwt_secret': new_secret}}
        )
        return res['updatedExisting']
