#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Filter(object):
    """Class for complex filtering.

    Except for simple filtering by query parameters, two more complex
    filtering schemes are to be supported:

    1. user-defined methods (supported now)

        a. override `query` method
        b. add `query_<name>` method

        All methods should return MongoDB-style conditions.

    2. `filter` keyword in query string (not supported yet)

        for example:
        <resource>/?filter=name==russell and age>=int(10) and date_joined<datetime(2014-10-10T11:40:00Z)

        Value string of `filter` will be parsed as MongoDB-style conditions.
    """

    def __init__(self, **kwargs):
        self.db = kwargs.get('db')
        self.table_name = kwargs.get('table_name')

    def query(self, query_params):
        conditions = {}
        for attr_name in dir(self):
            if attr_name.startswith('query_'):
                method = getattr(self, attr_name)
                conditions.update(method(query_params))
        conditions.update(query_params)
        return conditions
