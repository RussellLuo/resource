#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import request, current_app as app
from flask.views import MethodView
from rsrc.utils import normalize_uri

from .view import ProxyView


def payload(request):
    """ Performs sanity checks or decoding depending on the Content-Type,
    then returns the request payload as a dict. If request Content-Type is
    unsupported, aborts with a 400 (Bad Request).

    Borrowed from `eve` - https://github.com/nicolaiarocci/eve
    """
    content_type = request.headers.get('Content-Type', '').split(';')[0]

    if content_type == 'application/json':
        return request.get_json()
    elif content_type == 'application/x-www-form-urlencoded':
        return request.form.to_dict() if len(request.form) else {}
    elif content_type == 'multipart/form-data':
        # as multipart is also used for file uploads, we let an empty
        # request.form go through as long as there are also files in the
        # request.
        if len(request.form) or len(request.files):
            # merge form fields and request files, so we get a single payload
            # to be validated against the resource schema.

            # list() is needed because Python3 items() returns a dict_view, not
            # a list as in Python2.
            return dict(list(request.form.to_dict().items()) +
                        list(request.files.to_dict().items()))
        else:
            return {}
    else:
        return {}


def make_view(view):
    class View(ProxyView, MethodView):

        def __init__(self):
            self.view = view

        def get_uri(self, request):
            return request.url

        def get_query_params(self, request):
            params = {
                k: v if len(v) > 1 else v[0]
                for k, v in request.args.iterlists()
            }
            return params

        def get_auth_params(self, request):
            auth = request.authorization
            if auth is None:
                return None
            return {
                'username': auth.username,
                'password': auth.password
            }

        def get_data(self, request):
            return payload(request)

        def make_response(self, data, status, headers):
            return app.make_response((data, status, headers))

        def dispatch_request(self, *args, **kwargs):
            """Override to add additional `request` parameter to meth()."""
            args = (request,) + args
            return super(View, self).dispatch_request(*args, **kwargs)

    return View


def get_args(resource):
    uri = resource.uri.rstrip('/')
    endpoint = str(resource.name)
    view_cls = make_view(resource.view)
    view_func = view_cls.as_view(endpoint)
    return uri, endpoint, view_func


def add_resource(app, resource, pk='pk'):
    uri, endpoint, view_func = get_args(resource)

    app.add_url_rule(normalize_uri(uri), view_func=view_func,
                     methods=['OPTIONS', 'GET', 'POST', 'DELETE'])
    app.add_url_rule(normalize_uri('%s/<%s>' % (uri, pk)), view_func=view_func,
                     methods=['OPTIONS', 'GET', 'PUT', 'PATCH', 'DELETE'])


def make_root(app, resource, pk='pk'):
    uri, endpoint, view_func = get_args(resource)

    app.add_url_rule(normalize_uri(uri), view_func=view_func, methods=['GET'])
