#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from datetime import datetime

from bson import ObjectId


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


SERIALIZE_SCHEMA = {
    'objectid': lambda value: str(value),
    'datetime': lambda value: value.strftime(DATE_FORMAT)
}


DESERIALIZE_SCHEMA = {
    'objectid': lambda value: ObjectId(value),
    'datetime': lambda value: datetime.strptime(value, DATE_FORMAT)
}


class Serializer(object):

    structure = {}

    def convert(self, schema, structure, data):
        assert isinstance(structure, dict), \
               '`structure` must a dict'

        if not (structure and isinstance(data, dict) and data):
            return data

        # do type conversion
        converted = copy.deepcopy(data)
        for k, v in structure.items():
            if v in schema:
                names = k.split('.')
                last = names[-1]
                field = converted
                try:
                    for name in names[:-1]:
                        field = field[name]
                    field[last] = schema[v](field[last])
                except KeyError:  # ignore non-existent keys
                    pass

        return converted

    def serialize(self, data):
        return self.convert(SERIALIZE_SCHEMA, self.structure, data)

    def deserialize(self, data):
        return self.convert(DESERIALIZE_SCHEMA, self.structure, data)
