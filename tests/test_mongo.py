#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

import requests
import json
from pymongo import MongoClient
from bson import ObjectId


URI = 'http://127.0.0.1:5000/users'


class MongoUserTest(unittest.TestCase):

    def setUp(self):
        self.db = MongoClient().test

        self.id = str(self.db.user.insert({
            'name': 'russell',
            'password': '123456',
            'date_joined': datetime(2014, 9, 27)
        }))

        self.extra_ids = [
            str(self.db.user.insert({
                'name': 'user_%d' % i,
                'password': '123456',
                'date_joined': datetime(2014, 10, i)
            }))
            for i in xrange(1, 9)
        ]

        self.headers = {'content-type': 'application/json'}

    def tearDown(self):
        self.db.user.remove()

    def test_get(self):
        resp = requests.get(URI)

        # validate response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 9)

    def test_get_by_simple_filter(self):
        query_params = ['name=user_1']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_params)))

        # validate response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            [{
                '_id': self.extra_ids[0],
                'name': 'user_1',
                'password': '123456',
                'date_joined': '2014-10-01T00:00:00Z'
            }]
        )

    def test_get_by_complex_filter(self):
        query_params = ['date_joined_gt=datetime(2014-10-01T00:00:00Z)',
                        'date_joined_lt=datetime(2014-10-03T00:00:00Z)']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_params)))

        # validate response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            [{
                '_id': self.extra_ids[1],
                'name': 'user_2',
                'password': '123456',
                'date_joined': '2014-10-02T00:00:00Z'
            }]
        )

    def test_get_by_sort(self):
        query_params = ['sort=date_joined']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_params)))

        # validate response
        self.assertEqual(resp.status_code, 200)
        expection = [{
            '_id': self.id,
            'name': 'russell',
            'password': '123456',
            'date_joined': '2014-09-27T00:00:00Z'
        }]
        expection.extend([
            {
                '_id': self.extra_ids[i - 1],
                'name': 'user_%d' % i,
                'password': '123456',
                'date_joined': '2014-10-0%dT00:00:00Z' % i
            }
            for i in xrange(1, 9)
        ])
        self.assertEqual(resp.json(), expection)

    def test_get_by_fields(self):
        query_params = ['sort=date_joined', 'fields=name,password']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_params)))

        # validate response
        self.assertEqual(resp.status_code, 200)
        expection = [{
            'name': 'russell',
            'password': '123456',
        }]
        expection.extend([
            {
                'name': 'user_%d' % i,
                'password': '123456',
            }
            for i in xrange(1, 9)
        ])
        self.assertEqual(resp.json(), expection)

    def test_post(self):
        data = {
            'name': 'tracey',
            'password': '123456',
            'date_joined': 'datetime(2014-09-27T00:00:00Z)'
        }
        resp = requests.post(URI, data=json.dumps(data), headers=self.headers)

        # validate response
        self.assertEqual(resp.status_code, 201)
        self.assertTrue('_id' in resp.json())

        # validate database
        _id = resp.json()['_id']
        user = self.db.user.find_one({'_id': ObjectId(_id)})
        self.assertEqual(
            user,
            {
                '_id': ObjectId(_id),
                'name': 'tracey',
                'password': '123456',
                'date_joined': datetime(2014, 9, 27)
            }
        )

    def test_put(self):
        data = {
            'name': 'russellluo',
            'password': '12345678',
            'date_joined': 'datetime(2014-09-28T00:00:00Z)'
        }
        resp = requests.put('%s/%s' % (URI, self.id),
                            data=json.dumps(data), headers=self.headers)

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user = self.db.user.find_one({'_id': ObjectId(self.id)})
        self.assertEqual(
            user,
            {
                '_id': ObjectId(self.id),
                'name': 'russellluo',
                'password': '12345678',
                'date_joined': datetime(2014, 9, 28)
            }
        )

    def test_patch(self):
        data = [
            {'op': 'add', 'path': '/password', 'value': '123**678'},
            {'op': 'add', 'path': '/date_joined',
             'value': 'datetime(2014-09-28T22:00:00Z)'}
        ]
        resp = requests.patch('%s/%s' % (URI, self.id),
                               data=json.dumps(data), headers=self.headers)

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user = self.db.user.find_one({'_id': ObjectId(self.id)})
        self.assertTrue(bool(user))
        self.assertEqual(user['password'], '123**678')
        self.assertEqual(user['date_joined'], datetime(2014, 9, 28, 22))

    def test_delete_one(self):
        _id = str(self.db.user.insert({
            'name': 'tracey2076',
            'password': '123456',
            'date_joined': datetime(2014, 9, 27)
        }))
        resp = requests.delete('%s/%s' % (URI, _id))

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user = self.db.user.find_one({'_id': ObjectId(_id)})
        self.assertFalse(bool(user))

    def test_delete_all(self):
        resp = requests.delete(URI)

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user_count = self.db.user.count()
        self.assertEqual(user_count, 0)


if __name__ == '__main__':
    unittest.main()
