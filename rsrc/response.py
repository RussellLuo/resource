#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Response(object):
    def __init__(self, data='', status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def __str__(self):
        return '<Response [{}]>'.format(self.status)

    def __unicode__(self):
        return unicode(self.__str__())

    __repr__ = __str__
