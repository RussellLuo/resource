#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .response import Response
from .exceptions import RSRCException


def serialized(arg):
    def wrapper(method):
        def decorator(self, **kwargs):
            # deserialize special arguments from request
            if arg in kwargs:
                kwargs[arg] = self.serializer.deserialize(kwargs[arg])

            try:
                response = method(self, **kwargs)
            except RSRCException as e:
                return Response(e.detail, e.status_code)

            # serialize special arguments from respsone
            if isinstance(response.content, (list, tuple)):
                response.content = map(self.serializer.serialize,
                                       response.content)
            else:
                response.content = self.serializer.serialize(response.content)

            return response
        return decorator
    return wrapper


class View(object):

    def __init__(self, form_cls, serializer, **kwargs):
        self.form_cls = form_cls
        self.serializer = serializer
        self.__dict__.update(kwargs)

    @serialized('filter_')
    def get_proxy(self, pk=None, filter_=None):
        return self.get(pk, filter_)

    @serialized('data')
    def post_proxy(self, data):
        return self.post(data)

    @serialized('data')
    def put_proxy(self, pk, data):
        return self.put(pk, data)

    @serialized('data')
    def patch_proxy(self, pk, data):
        return self.patch(pk, data)

    def delete_proxy(self, pk):
        return self.delete(pk)

    def get(self, pk=None, filter_=None):
        raise NotImplementedError()

    def post(self, data):
        raise NotImplementedError()

    def put(self, pk, data):
        raise NotImplementedError()

    def patch(self, pk, data):
        raise NotImplementedError()

    def delete(self, pk):
        raise NotImplementedError()
