#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

import requests
import json
from pymongo import MongoClient
from bson import ObjectId


URI = 'http://127.0.0.1:5000/users/'


class MongoUserTest(unittest.TestCase):

    def setUp(self):
        self.db = MongoClient().test

        self.id = str(self.db.user.insert({
            'name': 'russell',
            'password': '123456',
            'date_joined': datetime(2014, 9, 27)
        }))

        self.headers = {'content-type': 'application/json'}

    def tearDown(self):
        self.db.user.remove()

    def test_get(self):
        resp = requests.get(URI)

        # validate response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            [{
                '_id': self.id,
                'name': 'russell',
                'password': '123456',
                'date_joined': '2014-09-27 00:00:00'
            }]
        )

    def test_post(self):
        data = {
            'name': 'tracey',
            'password': '123456',
            'date_joined': 'datetime(2014-09-27 00:00:00)'
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
            'date_joined': 'datetime(2014-09-28 00:00:00)'
        }
        resp = requests.put('%s%s/' % (URI, self.id),
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
             'value': 'datetime(2014-09-28 22:00:00)'}
        ]
        resp = requests.patch('%s%s/' % (URI, self.id),
                               data=json.dumps(data), headers=self.headers)

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user = self.db.user.find_one({'_id': ObjectId(self.id)})
        self.assertTrue(bool(user))
        self.assertEqual(user['password'], '123**678')
        self.assertEqual(user['date_joined'], datetime(2014, 9, 28, 22))

    def test_delete(self):
        _id = str(self.db.user.insert({
            'name': 'tracey2076',
            'password': '123456',
            'date_joined': datetime(2014, 9, 27)
        }))
        resp = requests.delete('%s%s/' % (URI, _id))

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user = self.db.user.find_one({'_id': ObjectId(_id)})
        self.assertFalse(bool(user))


if __name__ == '__main__':
    unittest.main()
