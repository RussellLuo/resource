#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import unittest
from datetime import datetime

import requests
import json
from pymongo import MongoClient


DOMAIN = 'http://127.0.0.1:5000'


class TestBase(unittest.TestCase):

    TOKEN_URI = DOMAIN + '/tokens/'
    USER_URI = DOMAIN + '/users/'

    def setUp(self):
        self.db = MongoClient().test

        self.db.user.insert({
            'username': 'russell',
            'password': '123456',
            'date_joined': datetime(2014, 10, 25),
            'jwt_secret': str(uuid.uuid4())
        })

        self.headers = {'content-type': 'application/json'}

    def tearDown(self):
        self.db.user.remove()

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        resp = requests.post(self.TOKEN_URI, data=json.dumps(data),
                             headers=self.headers)
        return resp.json()


class TokenTest(TestBase):

    def test_get_valid_token(self):
        token = self.login('russell', '123456')
        self.assertNotEqual(token['token'], None)
        self.assertEqual(token['expires'], 3600)

    def test_get_invalid_token(self):
        token = self.login('russell', 'error_password')
        self.assertEqual(token['token'], None)
        self.assertEqual(token['expires'], 0)


class UserTest(TestBase):

    def test_get_without_token(self):
        resp = requests.get(self.USER_URI)
        self.assertEqual(resp.status_code, 401)

    def test_get_with_valid_token(self):
        token = self.login('russell', '123456')
        resp = requests.get(self.USER_URI, auth=(token['token'], ''))
        self.assertEqual(resp.status_code, 200)

    def test_get_with_invalid_token(self):
        resp = requests.get(self.USER_URI, auth=('anonymous', ''))
        self.assertEqual(resp.status_code, 401)

    def test_post(self):
        """Everyone can POST."""
        data = {
            'username': 'tracey',
            'password': '123456',
            'date_joined': 'datetime(2014-10-25T00:00:00Z)'
        }
        resp = requests.post(self.USER_URI, data=json.dumps(data),
                             headers=self.headers)

        self.assertEqual(resp.status_code, 201)


if __name__ == '__main__':
    unittest.main()
