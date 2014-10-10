#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import Serializer
from resource.shared_schema import (
    get_serialize_schema, get_deserialize_schema
)


class MongoSerializer(Serializer):

    serialize_schema = get_serialize_schema(['objectid', 'datetime'])

    deserialize_schema = get_deserialize_schema([
        'int', 'bool', 'objectid', 'datetime'
    ])
