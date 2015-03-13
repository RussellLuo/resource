#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rsrc import Filter


class DuFilter(Filter):
    """Double-underscore style filtering."""

    separator = '__'

    def get_du_params(self, params, suffix):
        """Get double-underscore style parameters which match `suffix`.

        For example:
            params: {'age__lt': 20, 'age__gt': 10, 'level__lt': 5}
            suffix: 'lt' => du_params: {'age': 20, 'level': 5}
            suffix: 'gt' => du_params: {'age': 10}
        """
        keys = [
            key for key in params
            if key.endswith(self.separator + suffix)
        ]
        du_params = {
            key.split(self.separator)[0]: params.pop(key)
            for key in keys
        }
        return du_params

    def get_conditions(self, params, suffix, comparer, convertor=None):
        if convertor is None:
            convertor = lambda v: v

        du_params = self.get_du_params(params, suffix)
        conditions = {
            key: {comparer: convertor(value)}
            for key, value in du_params.items()
        }
        return conditions

    def query_ne(self, params):
        """Query by keyword `<fieldname>__ne`.

        For example:
            /?age__ne=int(20) <=> {'age': {'$ne': 20}}
        """
        return self.get_conditions(params, 'ne', '$ne')

    def query_lt(self, params):
        """Query by keyword `<fieldname>__lt`.

        For example:
            /?age__lt=int(20) <=> {'age': {'$lt': 20}}
        """
        return self.get_conditions(params, 'lt', '$lt')

    def query_lte(self, params):
        """Query by keyword `<fieldname>__lte`.

        For example:
            /?age__lte=int(20) <=> {'age': {'$lte': 20}}
        """
        return self.get_conditions(params, 'lte', '$lte')

    def query_gt(self, params):
        """Query by keyword `<fieldname>__gt`.

        For example:
            /?age__gt=int(20) <=> {'age': {'$gt': 20}}
        """
        return self.get_conditions(params, 'gt', '$gt')

    def query_gte(self, params):
        """Query by keyword `<fieldname>__gte`.

        For example:
            /?age__gte=int(20) <=> {'age': {'$gte': 20}}
        """
        return self.get_conditions(params, 'gte', '$gte')

    def query_in(self, params):
        """Query by keyword `<fieldname>__in`.

        For example:
            /?age__in=int(20) <=> {'age': {'$in': [20]}}
            /?age__in=int(20)&age__in=int(25) <=> {'age': {'$in': [20, 25]}}
        """
        def make_list(value):
            if not isinstance(value, (tuple, list)):
                return [value]
            return value

        return self.get_conditions(params, 'in', '$in', make_list)

    def query_like(self, params):
        """Query by keyword `<fieldname>__like`.

        For example:
            /?name__like=^russ <=> {'name': {'$regex': '^russ'}}
        """
        return self.get_conditions(params, 'like', '$regex')
