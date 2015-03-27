#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from pymongo import MongoClient
from crest import Resource


API = Resource('http://127.0.0.1:5000')


class MongoUserTest(unittest.TestCase):

    def setUp(self):
        self.db = MongoClient().test
        self.ids = [
            str(self.db.user.insert({
                'username': 'user_%d' % i,
                'password': '123456',
                'date_joined': datetime(2014, 10, i)
            }))
            for i in xrange(1, 9)
        ]

    def tearDown(self):
        self.db.user.remove()

    def validate_response(self, resp, usernames):
        self.assertEqual(resp.status_code, 200)
        resp_usernames = [r['username'] for r in resp.json()]
        self.assertEqual(resp_usernames, usernames)

    def test_get_by_eq(self):
        query_params = {'username': 'user_1'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_1'])

    def test_get_by_ne(self):
        query_params = {'username__ne': 'user_1'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_%s' % i for i in xrange(2, 9)])

    def test_get_by_lt(self):
        query_params = {'date_joined__lt': 'datetime(2014-10-02T00:00:00Z)'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_1'])

    def test_get_by_lte(self):
        query_params = {'date_joined__lte': 'datetime(2014-10-02T00:00:00Z)'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_1', 'user_2'])

    def test_get_by_gt(self):
        query_params = {'date_joined__gt': 'datetime(2014-10-07T00:00:00Z)'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_8'])

    def test_get_by_gte(self):
        query_params = {'date_joined__gte': 'datetime(2014-10-07T00:00:00Z)'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_7', 'user_8'])

    def test_get_by_in(self):
        query_params = {'username__in': ['user_1', 'user_2']}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_1', 'user_2'])

    def test_get_by_like(self):
        query_params = {'username__like': '_1$'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_1'])

    def test_get_by_gt_and_lt(self):
        query_params = {'date_joined__gt': 'datetime(2014-10-06T00:00:00Z)',
                        'date_joined__lt': 'datetime(2014-10-08T00:00:00Z)'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_7'])

    def test_get_by_gte_and_lte(self):
        query_params = {'date_joined__gte': 'datetime(2014-10-06T00:00:00Z)',
                        'date_joined__lte': 'datetime(2014-10-08T00:00:00Z)'}
        resp = API.users.get(params=query_params)
        self.validate_response(resp, ['user_6', 'user_7', 'user_8'])


if __name__ == '__main__':
    unittest.main()
