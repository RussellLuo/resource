#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Response(object):
    def __init__(self, content='', status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}
