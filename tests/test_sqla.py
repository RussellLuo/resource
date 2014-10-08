#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

import requests
import json
import sqlsoup
from sqlalchemy import create_engine


URI = 'http://127.0.0.1:5000/users/'


class SqlaUserTest(unittest.TestCase):

    def setUp(self):
        # increase connection timeout of SQlite
        # see http://stackoverflow.com/questions/15065037/how-to-increase-connection-timeout-using-sqlalchemy-with-sqlite-in-python
        self.db = sqlsoup.SQLSoup(create_engine(
            'sqlite:///sqlite.db', connect_args={'timeout': 15}
        ))

        row = self.db.user.insert(
            name='russell',
            password='123456',
            date_joined=datetime(2014, 9, 27)
        )
        self.db.commit()
        self.id = row.id

        self.extra_ids = []
        for i in xrange(1, 9):
            row = self.db.user.insert(
                name='user_%d' % i,
                password='123456',
                date_joined=datetime(2014, 10, i)
            )
            self.db.commit()
            self.extra_ids.append(row.id)

        self.headers = {'content-type': 'application/json'}

    def tearDown(self):
        self.db.user.delete()
        self.db.commit()

    def test_get(self):
        resp = requests.get(URI)

        # validate response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 9)

    def test_get_filter(self):
        query_string = ['name=user_1']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_string)))

        # validate response
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            [{
                'id': self.extra_ids[0],
                'name': 'user_1',
                'password': '123456',
                'date_joined': '2014-10-01 00:00:00'
            }]
        )

    def test_get_sort(self):
        query_string = ['sort=date_joined']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_string)))

        # validate response
        self.assertEqual(resp.status_code, 200)
        expection = [{
            'id': self.id,
            'name': 'russell',
            'password': '123456',
            'date_joined': '2014-09-27 00:00:00'
        }]
        expection.extend([
            {
                'id': self.extra_ids[i - 1],
                'name': 'user_%d' % i,
                'password': '123456',
                'date_joined': '2014-10-0%d 00:00:00' % i
            }
            for i in xrange(1, 9)
        ])
        self.assertEqual(resp.json(), expection)

    def test_get_fields(self):
        query_string = ['sort=date_joined', 'fields=name,password']
        resp = requests.get('%s?%s' % (URI, '&'.join(query_string)))

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
            'date_joined': 'datetime(2014-09-27 00:00:00)'
        }
        resp = requests.post(URI, data=json.dumps(data), headers=self.headers)

        # validate response
        self.assertEqual(resp.status_code, 201)
        self.assertTrue('id' in resp.json())

        # validate database
        _id = int(resp.json()['id'])
        user = self.db.user.filter_by(id=_id).first()
        self.assertEqual(user.id, _id)
        self.assertEqual(user.name, 'tracey')
        self.assertEqual(user.password, '123456')
        self.assertEqual(user.date_joined, datetime(2014, 9, 27))

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
        user = self.db.user.filter_by(id=self.id).first()
        self.assertEqual(user.id, self.id)
        self.assertEqual(user.name, 'russellluo')
        self.assertEqual(user.password, '12345678')
        self.assertEqual(user.date_joined, datetime(2014, 9, 28))

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
        user = self.db.user.filter_by(id=self.id).first()
        self.assertTrue(bool(user))
        self.assertEqual(user.password, '123**678')
        self.assertEqual(user.date_joined, datetime(2014, 9, 28, 22))

    def test_delete(self):
        row = self.db.user.insert(
            name='tracey2076',
            password='123456',
            date_joined=datetime(2014, 9, 27)
        )
        self.db.commit()
        _id = row.id
        resp = requests.delete('%s%s/' % (URI, _id))

        # validate response
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.text, '')

        # validate database
        user = self.db.user.filter_by(id=_id).first()
        self.assertFalse(bool(user))


if __name__ == '__main__':
    unittest.main()
