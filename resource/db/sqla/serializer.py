#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from resource import settings, Serializer


class SqlaSerializer(Serializer):

    serialize_schema = {
        datetime: lambda value: value.strftime(settings.DATE_FORMAT)
    }

    deserialize_schema = {
        'datetime': lambda value: datetime.strptime(value,
                                                    settings.DATE_FORMAT)
    }
