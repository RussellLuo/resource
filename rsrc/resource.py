#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .conf import settings
from .form import Form
from .filter import Filter
from .utils import import_object, normalize_uri


class Resource(object):
    def __init__(self, name, view_cls, uri='', serializer=None,
                 form_cls=Form, filter_cls=Filter,
                 auth_cls=None, kwargs=None):
        kwargs = kwargs or {}
        self.name = name
        self.uri = normalize_uri(uri or '/%s' % name)
        auth_cls = auth_cls or import_object(settings.AUTH)
        self.view = view_cls(self.uri, serializer, form_cls,
                             filter_cls, auth_cls, **kwargs)
