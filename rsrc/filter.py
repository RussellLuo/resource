#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import functools


def query_params(*names):
    """A helper decorator for binding query-params specified by
    `names` as arguments to `query_<name>` methods.

    For example:

        class UserFilter(Filter):
            @query_params('username')
            def query_username(self, username):
                return {'username': username.upper()}

            @query_params('date_joined_gt', 'date_joined_lt')
            def query_datejoined(self, date_joined_gt=None, date_joined_lt=None):
                conditions = {}
                if date_joined_gt:
                    conditions.update({'$gt': date_joined_gt})
                if date_joined_lt:
                    conditions.update({'$lt': date_joined_lt})
                if conditions:
                    return {'date_joined': conditions}
                else:
                    return {}
    """
    def wrapper(method):
        @functools.wraps(method)
        def decorator(self, params):
            kwargs = {}
            for name in names:
                if name in params:
                    value = params.pop(name)
                    kwargs.update({name: value})
            try:
                return method(self, **kwargs)
            except TypeError:
                return {}
        return decorator

    return wrapper


class Filter(object):
    """The Class for complex filtering.

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

    def merge(self, conditions):
        """Merge `conditions` using AND-logic into one condition."""
        if conditions:
            return {'$and': conditions}
        else:
            return {}

    def query(self, params):
        """Generate lookup conditions."""
        params = copy.deepcopy(params)
        conditions = []

        # collect conditions from `query_<name>` methods
        for attr_name in dir(self):
            if attr_name.startswith('query_'):
                method = getattr(self, attr_name)
                condition = method(params)
                if condition:
                    conditions.append(condition)

        # also treat remaining `params` as conditions
        if params:
            conditions.append(params)

        return self.merge(conditions)
