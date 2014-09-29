#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import View, Response


class Index(View):
    """Index of resources."""

    def __init__(self, *arg, **kwargs):
        super(Index, self).__init__(*arg, **kwargs)
        self.links = (
            {'href': r.uri, 'title': r.name}
            for r in self.resources
        )

    def get_items(self, page, per_page, filter_):
        return Response(list(self.links))
