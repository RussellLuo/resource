#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from .conf import settings
from .response import Response
from .exceptions import BaseError, NotFoundError, MethodNotAllowedError
from .logger import logger


def serialized(method):
    @functools.wraps(method)
    def decorator(self, request, **kwargs):
        # deserialize special arguments from request
        if self.serializer:
            request.data = self.serializer.deserialize(request.data)
            request.query_params = self.serializer.deserialize(
                request.query_params
            )

        # log request info
        if request.method in settings.LOGGER_METHODS:
            message = '%s %s %s' % (request.method, request.uri, request.data)
            logger.info(message)

        try:
            response = method(self, request, **kwargs)
        except BaseError as e:
            data = {'message': e.detail}
            response = Response(data, e.status_code, e.headers)

        # serialize special arguments from response
        if self.serializer:
            response.data = self.serializer.serialize(
                response.data, settings.WITH_TYPE_NAME
            )

        # add essential headers for non-OPTIONS requests if in CORS
        if settings.CROSS_ORIGIN and request.method != 'OPTIONS':
            _, actual_headers = self.make_cross_origin_headers()
            response.headers.update(actual_headers)

        # log response info
        if request.method in settings.LOGGER_METHODS:
            message = '%s %s' % (response.status, response.data)
            logger.info(message)

        return response
    return decorator


class View(object):

    def __init__(self, uri, serializer, form_cls,
                 filter_cls, auth_cls, **kwargs):
        self.uri = uri
        self.serializer = serializer
        self.form_cls = form_cls
        self.filter = filter_cls(**kwargs)
        self.auth = auth_cls()
        self.__dict__.update(kwargs)

    def get_pagination_args(self, query_params):
        PAGE = 1
        PER_PAGE = settings.PER_PAGE

        try:
            page = int(query_params.pop('page', None))
            if page < 1:
                page = PAGE
        except Exception:
            page = PAGE

        try:
            per_page = int(query_params.pop('per_page', None))
            if per_page < 1:
                per_page = PER_PAGE
        except Exception:
            per_page = PER_PAGE

        return page, per_page

    def make_pagination_headers(self, page, per_page, count):
        headers = {}

        div, mod = divmod(count, per_page)
        page_count = div + int(mod > 0)

        links = []

        def add_link(page, per_page, rel):
            args = (settings.DOMAIN_NAME, self.uri, page, per_page, rel)
            links.append('<%s%s?page=%s&per_page=%s>; rel="%s"' % args)

        def add_prev_link():
            add_link(page - 1, per_page, 'prev')

        def add_next_link():
            add_link(page + 1, per_page, 'next')

        def add_first_link():
            add_link(1, per_page, 'first')

        def add_last_link():
            add_link(page_count, per_page, 'last')

        # fill `Link` headers
        if page_count > 0 and page != page_count:
            if page == 1:
                add_next_link()
                add_last_link()
            elif page < page_count:
                add_prev_link()
                add_next_link()
                add_first_link()
                add_last_link()
            elif page == page_count:
                add_prev_link()
                add_first_link()
            else:
                add_link(page_count, per_page, 'prev')
                add_first_link()
                add_last_link()

            headers.update({'Link': ', '.join(links)})

        # fill `X-Pagination-Info` headers
        args = (page, per_page, count)
        headers.update({
            'X-Pagination-Info': 'page=%s, per-page=%s, count=%s' % args
        })

        return headers

    def get_sort_args(self, query_params):
        sort = query_params.pop('sort', None)
        if sort is None:
            args = None
        else:
            args = [
                (arg[1:], -1) if arg.startswith('-') else (arg, 1)
                for arg in sort.split(',')
            ]
        return args

    def get_fields_selected(self, query_params):
        fields = query_params.pop('fields', None)
        if fields is None:
            selected = None
        else:
            selected = fields.split(',')
        return selected

    def make_cross_origin_headers(self, allow_origin=None, allow_methods=None,
                                  allow_headers=None, max_age=None):
        allow_origin = allow_origin or settings.ACCESS_CONTROL_ALLOW_ORIGIN
        allow_methods = allow_methods or settings.ACCESS_CONTROL_ALLOW_METHODS
        allow_headers = allow_headers or settings.ACCESS_CONTROL_ALLOW_HEADERS
        max_age = max_age or settings.ACCESS_CONTROL_MAX_AGE
        vary = 'Origin'

        # the response headers for preflight requests
        preflight_headers = {
            'Access-Control-Allow-Origin': allow_origin,
            'Access-Control-Allow-Methods': ', '.join(allow_methods),
            'Access-Control-Allow-Headers': ', '.join(allow_headers),
            'Access-Control-Max-Age': str(max_age),
            'Vary': vary,
        }

        # the response headers for actual requests
        actual_headers = {
            'Access-Control-Allow-Origin': allow_origin,
            'Vary': vary,
        }

        return preflight_headers, actual_headers

    def options_proxy(self, request, **kwargs):
        return self.options(request, **kwargs)

    @serialized
    def get_proxy(self, request, **kwargs):
        method = 'GET_LIST' if kwargs.get('pk') is None else 'GET_ITEM'
        self.auth.check_auth(method, request.kwargs['auth'])
        return self.get(request, **kwargs)

    @serialized
    def post_proxy(self, request, **kwargs):
        self.auth.check_auth('POST', request.kwargs.get('auth'))
        return self.post(request, **kwargs)

    @serialized
    def put_proxy(self, request, **kwargs):
        self.auth.check_auth('PUT', request.kwargs.get('auth'))
        return self.put(request, **kwargs)

    @serialized
    def patch_proxy(self, request, **kwargs):
        self.auth.check_auth('PATCH', request.kwargs.get('auth'))
        return self.patch(request, **kwargs)

    @serialized
    def delete_proxy(self, request, **kwargs):
        method = 'DELETE_LIST' if kwargs.get('pk') is None else 'DELETE_ITEM'
        self.auth.check_auth(method, request.kwargs.get('auth'))
        return self.delete(request, **kwargs)

    def get_pk(self, pk):
        raise NotFoundError()

    def options(self, request, **kwargs):
        headers = {
            'Allow': 'GET, POST, PUT, PATCH, DELETE'
        }
        if settings.CROSS_ORIGIN:
            preflight_headers, _ = self.make_cross_origin_headers()
            headers.update(preflight_headers)
        return Response(headers=headers)

    def get(self, request, **kwargs):
        if kwargs.get('pk') is None:
            query_params = request.query_params
            page, per_page = self.get_pagination_args(query_params)
            request.kwargs.update(
                page=page,
                per_page=per_page,
                sort=self.get_sort_args(query_params),
                fields=self.get_fields_selected(query_params),
                lookup=self.filter.query(query_params)
            )
            return self.get_list(request, **kwargs)
        else:
            return self.get_item(request, **kwargs)

    def get_list(self, request, **kwargs):
        raise MethodNotAllowedError()

    def get_item(self, request, **kwargs):
        raise MethodNotAllowedError()

    def post(self, request, **kwargs):
        raise MethodNotAllowedError()

    def put(self, request, **kwargs):
        raise MethodNotAllowedError()

    def patch(self, request, **kwargs):
        raise MethodNotAllowedError()

    def delete(self, request, **kwargs):
        if kwargs.get('pk') is None:
            return self.delete_list(request, **kwargs)
        else:
            return self.delete_item(request, **kwargs)

    def delete_list(self, request, **kwargs):
        raise MethodNotAllowedError()

    def delete_item(self, request, **kwargs):
        raise MethodNotAllowedError()
