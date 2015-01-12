#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Request(object):
    def __init__(self, method='GET', data=None, query_params=None,
                 headers=None, kwargs=None):
        self.method = method
        self.data = data or {}
        self.query_params = query_params or {}
        self.headers = headers or {}
        self.kwargs = kwargs or {}
