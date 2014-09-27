#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from resource import Serializer


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class MongoSerializer(Serializer):

    serialize_schema = {
        'objectid': lambda value: str(value),
        'datetime': lambda value: value.strftime(DATE_FORMAT)
    }

    deserialize_schema = {
        'objectid': lambda value: ObjectId(value),
        'datetime': lambda value: datetime.strptime(value, DATE_FORMAT)
    }

    structure = {
        '_id': 'objectid'
    }
