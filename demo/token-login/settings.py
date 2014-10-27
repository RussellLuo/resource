#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

DOMAIN_NAME = 'http://localhost:5000'
TOKEN_USER = 'user.MongoTokenUser'

DB = MongoClient().test
