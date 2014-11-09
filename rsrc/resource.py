#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .conf import settings
from .form import Form
from .serializer import Serializer
from .filter import Filter
from .utils import import_object


class Resource(object):
    def __init__(self, name, view_cls, uri='', form_cls=Form,
                 serializer_cls=Serializer, filter_cls=Filter,
                 auth_cls=None, kwargs=None):
        kwargs = kwargs or {}
        self.name = name
        self.uri = uri or '/%s/' % name
        auth_cls = auth_cls or import_object(settings.AUTH)
        self.view = view_cls(self.uri, form_cls, serializer_cls,
                             filter_cls, auth_cls, **kwargs)
