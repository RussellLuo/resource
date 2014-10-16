#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import functools


def response(method):
    @functools.wraps(method)
    def decorator(self, *args, **kwargs):
        res = method(self, *args, **kwargs)
        content = json.dumps(res.content)
        res.headers.update({'Content-Type': 'application/json'})
        return self.make_response(content, res.status, res.headers)
    return decorator


class ProxyView(object):
    """Delegate requests from framework-view to resource-view.

    Subclasses of `ProxyView` should set the `view` attribute, and override
    the following methods:
        get_query_params
        get_auth_params
        get_data
        make_response
    """

    def get_query_params(self, request):
        raise NotImplementedError()

    def get_auth_params(self, request):
        raise NotImplementedError()

    def get_data(self, request):
        raise NotImplementedError()

    def make_response(self, content, status, headers):
        raise NotImplementedError()

    @response
    def get(self, request, pk=None):
        return self.view.get_proxy(
            pk=pk,
            query_params=self.get_query_params(request),
            auth_params=self.get_auth_params(request)
        )

    @response
    def post(self, request):
        return self.view.post_proxy(
            data=self.get_data(request),
            auth_params=self.get_auth_params(request)
        )

    @response
    def put(self, request, pk):
        return self.view.put_proxy(
            pk=pk,
            data=self.get_data(request),
            auth_params=self.get_auth_params(request)
        )

    @response
    def patch(self, request, pk):
        return self.view.patch_proxy(
            pk=pk,
            data=self.get_data(request),
            auth_params=self.get_auth_params(request)
        )

    @response
    def delete(self, request, pk):
        return self.view.delete_proxy(
            pk=pk,
            auth_params=self.get_auth_params(request)
        )
