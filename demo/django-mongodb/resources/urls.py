#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .resources import index, resources

from resource.contrib.framework.django import (
    get_resource_urlpatterns, get_index_urlpatterns
)


urlpatterns = get_index_urlpatterns(index)

for r in resources:
    urlpatterns += get_resource_urlpatterns(r)
