#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from .conf import settings
from .response import Response
from .exceptions import BaseError, NotFoundError, MethodNotAllowedError


def serialized(arg=None):
    def wrapper(method):
        @functools.wraps(method)
        def decorator(self, **kwargs):
            # deserialize special arguments from request
            if arg in kwargs:
                kwargs[arg] = self.serializer.deserialize(kwargs[arg])

            try:
                response = method(self, **kwargs)
            except BaseError as e:
                content = {'message': e.detail}
                return Response(content, e.status_code, e.headers)

            # serialize special arguments from response
            if isinstance(response.content, (list, tuple)):
                response.content = map(self.serializer.serialize,
                                       response.content)
            else:
                response.content = self.serializer.serialize(response.content)

            return response
        return decorator
    return wrapper


class View(object):

    def __init__(self, uri, form_cls, serializer_cls,
                 filter_cls, auth_cls, **kwargs):
        self.uri = uri
        self.form_cls = form_cls
        self.serializer = serializer_cls()
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
        if page != page_count:
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

    @serialized('query_params')
    def get_proxy(self, pk=None, query_params=None, auth_params=None):
        method = 'GET_LIST' if pk is None else 'GET_ITEM'
        self.auth.check_auth(method, auth_params)
        return self.get(pk, query_params)

    @serialized('data')
    def post_proxy(self, data, auth_params=None):
        self.auth.check_auth('POST', auth_params)
        return self.post(data)

    @serialized('data')
    def put_proxy(self, pk, data, auth_params=None):
        self.auth.check_auth('PUT', auth_params)
        return self.put(pk, data)

    @serialized('data')
    def patch_proxy(self, pk, data, auth_params=None):
        self.auth.check_auth('PATCH', auth_params)
        return self.patch(pk, data)

    @serialized()
    def delete_proxy(self, pk, auth_params=None):
        self.auth.check_auth('DELETE', auth_params)
        return self.delete(pk)

    def get_pk(self, pk):
        raise NotFoundError()

    def get(self, pk=None, query_params=None):
        if pk is None:
            query_params = query_params or {}
            page, per_page = self.get_pagination_args(query_params)
            sort = self.get_sort_args(query_params)
            fields = self.get_fields_selected(query_params)
            lookup = self.filter.query(query_params)
            return self.get_list(page, per_page, sort, fields, lookup)
        else:
            return self.get_item(pk)

    def get_list(self, page, per_page, sort, fields, lookup):
        raise MethodNotAllowedError()

    def get_item(self, pk):
        raise MethodNotAllowedError()

    def post(self, data):
        raise MethodNotAllowedError()

    def put(self, pk, data):
        raise MethodNotAllowedError()

    def patch(self, pk, data):
        raise MethodNotAllowedError()

    def delete(self, pk):
        raise MethodNotAllowedError()
