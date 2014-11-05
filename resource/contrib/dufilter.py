#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import Filter


class DuFilter(Filter):
    """Double-underscore style filtering."""

    separator = '__'

    def get_params(self, query_params, suffix):
        """Get parameters which have `suffix`.

        For example:
            query_params: {'age__lt': 20, 'age__gt': 10, 'level__lt': 5}
            suffix: 'lt' => params: {'age': 20, 'level': 5}
            suffix: 'gt' => params: {'age': 10}
        """
        keys = [
            key for key in query_params
            if key.endswith(self.separator + suffix)
        ]
        params = {
            key.split(self.separator)[0]: query_params.pop(key)
            for key in keys
        }
        return params

    def get_conditions(self, query_params, suffix, comparer, convertor=None):
        if convertor is None:
            convertor = lambda v: v

        params = self.get_params(query_params, suffix)
        conditions = {
            key: {comparer: convertor(value)}
            for key, value in params.items()
        }
        return conditions

    def query_ne(self, query_params):
        """Query by keyword `<fieldname>__ne`.

        For example:
            /?age__ne=int(20) <=> {'age': {'$ne': 20}}
        """
        return self.get_conditions(query_params, 'ne', '$ne')

    def query_lt(self, query_params):
        """Query by keyword `<fieldname>__lt`.

        For example:
            /?age__lt=int(20) <=> {'age': {'$lt': 20}}
        """
        return self.get_conditions(query_params, 'lt', '$lt')

    def query_lte(self, query_params):
        """Query by keyword `<fieldname>__lte`.

        For example:
            /?age__lte=int(20) <=> {'age': {'$lte': 20}}
        """
        return self.get_conditions(query_params, 'lte', '$lte')

    def query_gt(self, query_params):
        """Query by keyword `<fieldname>__gt`.

        For example:
            /?age__gt=int(20) <=> {'age': {'$gt': 20}}
        """
        return self.get_conditions(query_params, 'gt', '$gt')

    def query_gte(self, query_params):
        """Query by keyword `<fieldname>__gte`.

        For example:
            /?age__gte=int(20) <=> {'age': {'$gte': 20}}
        """
        return self.get_conditions(query_params, 'gte', '$gte')

    def query_in(self, query_params):
        """Query by keyword `<fieldname>__in`.

        For example:
            /?age__in=int(20) <=> {'age': {'$in': [20]}}
            /?age__in=int(20)&age__in=int(25) <=> {'age': {'$in': [20, 25]}}
        """
        def make_list(value):
            if not isinstance(value, (tuple, list)):
                return [value]
            return value

        return self.get_conditions(query_params, 'in', '$in', make_list)

    def query_like(self, query_params):
        """Query by keyword `<fieldname>__like`.

        For example:
            /?name__like=^russ <=> {'name': {'$regex': '^russ'}}
        """
        return self.get_conditions(query_params, 'like', '$regex')
