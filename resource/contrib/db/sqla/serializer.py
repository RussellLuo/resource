#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import Serializer
from ..shared_schema import (
    get_serialize_schema, get_deserialize_schema
)


class SqlaSerializer(Serializer):

    serialize_schema = get_serialize_schema(['datetime'])

    deserialize_schema = get_deserialize_schema(['int', 'bool', 'datetime'])
