#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from flask import request, current_app as app
from flask.views import MethodView


def payload():
    """ Performs sanity checks or decoding depending on the Content-Type,
    then returns the request payload as a dict. If request Content-Type is
    unsupported, aborts with a 400 (Bad Request).

    Borrowed from `eve` - https://github.com/nicolaiarocci/eve
    """
    content_type = request.headers['Content-Type'].split(';')[0]

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


def response(method):
    def decorator(*args, **kwargs):
        res = method(*args, **kwargs)
        content = json.dumps(res.content)
        return app.make_response((content, res.status,
                                 {'Content-Type': 'application/json'}))
    return decorator


def make_view(view):
    class View(MethodView):

        @response
        def get(self, pk=None):
            filter_ = request.args.to_dict()
            return view.get_proxy(pk=pk, filter_=filter_)

        @response
        def post(self):
            data = payload()
            return view.post_proxy(data=data)

        @response
        def put(self, pk):
            data = payload()
            return view.put_proxy(pk=pk, data=data)

        @response
        def patch(self, pk):
            data = payload()
            return view.patch_proxy(pk=pk, data=data)

        @response
        def delete(self, pk):
            return view.delete_proxy(pk=pk)

    return View


def add_resource(app, resource, pk='pk'):
    uri = resource.uri
    endpoint = str(resource.name)
    view = make_view(resource.view)
    view_func = view.as_view(endpoint)

    app.add_url_rule(uri, defaults={pk: None},
                     view_func=view_func, methods=['GET'])
    app.add_url_rule(uri, view_func=view_func, methods=['POST'])
    app.add_url_rule('%s<%s>/' % (uri, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'PATCH', 'DELETE'])
