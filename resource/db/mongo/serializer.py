#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import Serializer


class MongoSerializer(Serializer):
    structure = {
        '_id': 'objectid'
    }
