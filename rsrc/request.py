#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Request(object):
    def __init__(self, scheme, uri, method='GET', data=None,
                 query_params=None, headers=None, kwargs=None):
        self.scheme = scheme
        self.uri = uri
        self.method = method
        self.data = data or {}
        self.query_params = query_params or {}
        self.headers = headers or {}
        self.kwargs = kwargs or {}

    def __str__(self):
        return '<Request {!r} [{}]>'.format(str(self.uri), self.method)

    def __unicode__(self):
        return unicode(self.__str__())

    __repr__ = __str__
