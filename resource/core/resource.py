#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonform import JsonForm

from .serializer import Serializer


class UselessForm(JsonForm):
    schema = {}


class Resource(object):
    def __init__(self, name, view, uri='', form=UselessForm,
                 serializer=Serializer, model=None, kwargs=None):
        kwargs = kwargs or {}
        self.name = name
        self.uri = uri or '/%s/' % name
        self.view = view(self.uri, form, serializer(), **kwargs)
        self.model = model
