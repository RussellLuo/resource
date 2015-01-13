#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import functools

from rsrc import Request


def response(method):
    @functools.wraps(method)
    def decorator(self, *args, **kwargs):
        resp = method(self, *args, **kwargs)
        content = json.dumps(resp.content)
        resp.headers.update({'Content-Type': 'application/json'})
        return self.make_response(content, resp.status, resp.headers)
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

    def make_request(self, raw_request):
        request = Request(
            method=raw_request.method,
            data=self.get_data(raw_request),
            query_params=self.get_query_params(raw_request),
            kwargs=dict(auth=self.get_auth_params(raw_request))
        )
        return request

    @response
    def get(self, request, **kwargs):
        return self.view.get_proxy(self.make_request(request), **kwargs)

    @response
    def post(self, request, **kwargs):
        return self.view.post_proxy(self.make_request(request, **kwargs))

    @response
    def put(self, request, **kwargs):
        return self.view.put_proxy(self.make_request(request), **kwargs)

    @response
    def patch(self, request, **kwargs):
        return self.view.patch_proxy(self.make_request(request), **kwargs)

    @response
    def delete(self, request, **kwargs):
        return self.view.delete_proxy(self.make_request(request), **kwargs)
