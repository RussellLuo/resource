#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from bson import ObjectId

from resource import settings, Serializer


class MongoSerializer(Serializer):

    serialize_schema = {
        ObjectId: lambda value: str(value),
        datetime: lambda value: value.strftime(settings.DATE_FORMAT)
    }

    deserialize_schema = {
        'objectid': lambda value: ObjectId(value),
        'datetime': lambda value: datetime.strptime(value,
                                                    settings.DATE_FORMAT)
    }
