#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonform import JsonForm

from .serializer import Serializer
from .filter import Filter


class UselessForm(JsonForm):
    schema = {}


class Resource(object):
    def __init__(self, name, view_cls, uri='', form_cls=UselessForm,
                 serializer_cls=Serializer, filter_cls=Filter, kwargs=None):
        kwargs = kwargs or {}
        self.name = name
        self.uri = uri or '/%s/' % name
        self.view = view_cls(self.uri, form_cls, serializer_cls,
                             filter_cls, **kwargs)
