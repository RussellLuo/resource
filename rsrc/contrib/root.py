#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter

from rsrc import settings, View, Response
from rsrc.utils import normalize_uri


class Root(View):
    """Root of resources."""

    def __init__(self, *arg, **kwargs):
        super(Root, self).__init__(*arg, **kwargs)
        self.links = [
            {
                'href': normalize_uri(settings.DOMAIN_NAME + r.uri),
                'title': r.name
            }
            for r in self.resources
        ]

    def do_filtering(self, content, lookup):
        def filterer(item):
            condition = [
                item.get(k) == v
                for k, v in lookup.items()
            ]
            return all(condition)
        return filter(filterer, content)

    def do_paginating(self, content, page, per_page):
        start = (page - 1) * per_page
        end = start + per_page
        return content[start:end]

    def do_sorting(self, content, sort):
        if sort is None:
            return content

        # The following sorting algorithm is borrowed from `multikeysort` in
        # https://wiki.python.org/moin/SortingListsOfDictionaries?highlight=%28%28HowTo%7CSorting%29%29

        comparers = [
            (itemgetter(name), order)
            for name, order in sort
        ]

        def comparer(left, right):
            for fn, mult in comparers:
                result = cmp(fn(left), fn(right))
                if result:
                    return mult * result
            else:
                return 0

        return sorted(content, cmp=comparer)

    def do_fields_selecting(self, content, fields):
        if fields is None:
            return content

        return [
            {
                k: v
                for k, v in item.items()
                if k in fields
            }
            for item in content
        ]

    def get_list(self, request):
        page = request.kwargs['page']
        per_page = request.kwargs['per_page']

        content = self.do_filtering(self.links, request.kwargs['lookup'])
        count = len(content)

        content = self.do_paginating(content, page, per_page)
        headers = self.make_pagination_headers(page, per_page, count)

        content = self.do_sorting(content, request.kwargs['sort'])
        content = self.do_fields_selecting(content, request.kwargs['fields'])

        return Response(content, headers=headers)
