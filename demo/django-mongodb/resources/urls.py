#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .resources import root, resources

from resource.contrib.framework.django import add_resource, make_root


urlpatterns = make_root(root)

for r in resources:
    urlpatterns += add_resource(r)
