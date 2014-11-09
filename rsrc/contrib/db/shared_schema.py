#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from datetime import datetime

from bson import ObjectId

from rsrc import settings


serialize_schema = {
    'regex': (re._pattern_type, lambda value: '/%s/' % value.pattern),
    'objectid': (ObjectId, lambda value: str(value)),
    'datetime': (datetime, lambda value: value.strftime(settings.DATE_FORMAT))
}


deserialize_schema = {
    'int': ('int', lambda value: int(value)),
    'bool': ('bool', lambda value: value == 'true'),
    'regex': ('regex', lambda value: re.compile(value[1:-1])),
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
