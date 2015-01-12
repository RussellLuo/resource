#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools

from .conf import settings
from .response import Response
from .exceptions import BaseError, NotFoundError, MethodNotAllowedError


def serialized(method):
    @functools.wraps(method)
    def decorator(self, request, *args, **kwargs):
        # deserialize special arguments from request
        if self.serializer:
            request.data = self.serializer.deserialize(request.data)
            request.query_params = self.serializer.deserialize(
                request.query_params
            )

        try:
            response = method(self, request, *args, **kwargs)
        except BaseError as e:
            content = {'message': e.detail}
            return Response(content, e.status_code, e.headers)

        # serialize special arguments from response
        if self.serializer:
            response.content = self.serializer.serialize(
                response.content, settings.WITH_TYPE_NAME
            )

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

    @serialized
    def get_proxy(self, request, pk=None):
        method = 'GET_LIST' if pk is None else 'GET_ITEM'
        self.auth.check_auth(method, request.kwargs['auth'])
        return self.get(request, pk)

    @serialized
    def post_proxy(self, request):
        self.auth.check_auth('POST', request.kwargs.get('auth'))
        return self.post(request)

    @serialized
    def put_proxy(self, request, pk):
        self.auth.check_auth('PUT', request.kwargs.get('auth'))
        return self.put(request, pk)

    @serialized
    def patch_proxy(self, request, pk):
        self.auth.check_auth('PATCH', request.kwargs.get('auth'))
        return self.patch(request, pk)

    @serialized
    def delete_proxy(self, request, pk):
        self.auth.check_auth('DELETE', request.kwargs.get('auth'))
        return self.delete(request, pk)

    def get_pk(self, pk):
        raise NotFoundError()

    def get(self, request, pk=None):
        if pk is None:
            query_params = request.query_params
            page, per_page = self.get_pagination_args(query_params)
            request.kwargs.update(
                page=page,
                per_page=per_page,
                sort=self.get_sort_args(query_params),
                fields=self.get_fields_selected(query_params),
                lookup=self.filter.query(query_params)
            )
            return self.get_list(request)
        else:
            return self.get_item(request, pk)

    def get_list(self, request):
        raise MethodNotAllowedError()

    def get_item(self, request, pk):
        raise MethodNotAllowedError()

    def post(self, request):
        raise MethodNotAllowedError()

    def put(self, request, pk):
        raise MethodNotAllowedError()

    def patch(self, request, pk):
        raise MethodNotAllowedError()

    def delete(self, request, pk):
        raise MethodNotAllowedError()
