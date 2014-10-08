#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from resource import Serializer


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class SqlaSerializer(Serializer):

    serialize_schema = {
        datetime: lambda value: value.strftime(DATE_FORMAT)
    }

    deserialize_schema = {
        'datetime': lambda value: datetime.strptime(value, DATE_FORMAT)
    }
