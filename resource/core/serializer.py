#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy


class Serializer(object):

    serialize_schema = {}

    deserialize_schema = {}

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
        return self.convert(self.serialize_schema, self.structure, data)

    def deserialize(self, data):
        return self.convert(self.deserialize_schema, self.structure, data)
