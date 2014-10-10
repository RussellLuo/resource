#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from resource import settings


serialize_schema = {
    'objectid': (ObjectId, lambda value: str(value)),
    'datetime': (datetime, lambda value: value.strftime(settings.DATE_FORMAT))
}


deserialize_schema = {
    'int': ('int', lambda value: int(value)),
    'bool': ('bool', lambda value: value == 'true'),
    'objectid': ('objectid', lambda value: ObjectId(value)),
    'datetime': ('datetime',
                 lambda value: datetime.strptime(value, settings.DATE_FORMAT))
}


def get_schema(schema, keys):
    return {
        v[0]: v[1]
        for k, v in schema.items()
        if k in keys
    }


def get_serialize_schema(keys):
    return get_schema(serialize_schema, keys)


def get_deserialize_schema(keys):
    return get_schema(deserialize_schema, keys)
