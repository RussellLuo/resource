#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import re


class Serializer(object):

    serialize_schema = {}

    deserialize_schema = {}

    def cast(self, cast_value, data):

        def cast_core(value):
            if isinstance(value, dict):
                return cast_dict(value)
            elif isinstance(value, list):
                return cast_list(value)
            else:
                return cast_value(value)

        def cast_dict(value):
            for k, v in value.items():
                value[k] = cast_core(v)
            return value

        def cast_list(value):
            for i, v in enumerate(value):
                value[i] = cast_core(v)
            return value

        backup = copy.deepcopy(data)
        return cast_core(backup)

    def serialize(self, data):

        def cast_value(value):
            schema = self.serialize_schema
            t = type(value)
            if t in schema:
                value = schema[t](value)
            return value

        return self.cast(cast_value, data)

    def deserialize(self, data):

        if sys.version_info[0] == 3:
            str_type = str
        else:
            str_type = basestring

        pattern = re.compile(r'(\w+)\((.*)\)')

        def cast_value(value):
            if isinstance(value, str_type):
                m = pattern.match(value)
                if m:
                    t, v = m.groups()
                    schema = self.deserialize_schema
                    if t in schema:
                        try:
                            value = schema[t](v)
                        except Exception:
                            pass
            return value

        return self.cast(cast_value, data)
