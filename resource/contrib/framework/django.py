#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import base64

from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls import patterns, url

from .view import ProxyView


HTTP_HEADER_ENCODING = 'iso-8859-1'


def get_authorization(request):
    """
    Inspired by `Django REST framework` - https://github.com/tomchristie/django-rest-framework
    """
    auth = request.META.get('HTTP_AUTHORIZATION')
    if not auth or auth[0].lower() != 'basic' or len(auth) != 2:
        return None

    try:
        auth_parts = (base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING)
                                               .partition(':'))
    except (TypeError, UnicodeDecodeError):
        return None

    return dict(username=auth_parts[0], password=auth_parts[2])


def payload(request):
    """
    Inspired by `Django REST framework` - https://github.com/tomchristie/django-rest-framework
    """

    # get the content body of the request, as a stream.
    try:
        content_length = int(request.META.get('CONTENT_LENGTH',
                             request.META.get('HTTP_CONTENT_LENGTH')))
    except (ValueError, TypeError):
        content_length = 0

    if content_length == 0:
        stream = None
    else:
        stream = request

    content_type = request.META.get('HTTP_CONTENT_TYPE',
                                    request.META.get('CONTENT_TYPE'))

    if stream is None or content_type is None:
        return {}

    encoding = settings.DEFAULT_CHARSET
    try:
        data = stream.read().decode(encoding)
        return json.loads(data)
    except ValueError:
        return {}


def make_view(view):
    class View(ProxyView, View):

        def __init__(self):
            self.view = view

        def get_query_params(self, request):
            return request.GET

        def get_auth_params(self, request):
            return get_authorization(request)

        def get_data(self, request):
            return payload(request)

        def make_response(self, content, status, headers):
            response = HttpResponse(content, status_code=status)
            for key, value in headers:
                response[key] = value
            return response

    return View


def get_args(resource):
    uri = resource.uri
    if uri.startswith('/'):
        uri = uri[1:]
    endpoint = str(resource.name)
    view_cls = make_view(resource.view)
    return uri, endpoint, view_cls


def url_rule(regex, view_cls, kwargs=None, methods=None):
    methods = methods or ['GET', 'POST', 'PUT', 'DELETE']
    methods = map(lambda m: m.lower(), methods)

    # set `http_method_names` on instance-level of `view_cls`
    # then, `self.http_method_names` will refer to `methods` here
    # so, HTTP methods not in `methods` will trigger 405 error.
    view = view_cls.as_view(http_method_names=methods)
    return url(regex, view, kwargs)


def get_resource_urlpatterns(resource, pk='pk'):
    uri, _, view_cls = get_args(resource)
    urlpatterns = patterns('',
        url_rule(r'^%s$' % uri, view_cls, {pk: None}, methods=['GET']),
        url_rule(r'^%s$' % uri, view_cls, methods=['POST']),
        url_rule(r'^%s(?P<pk>\w+)/$' % uri, view_cls,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    )
    return urlpatterns


def get_index_urlpatterns(resource, pk='pk'):
    uri, _, view_cls = get_args(resource)
    urlpatterns = patterns('',
        url_rule(r'^%s$' % uri, view_cls, {pk: None}, methods=['GET']),
    )
    return urlpatterns
