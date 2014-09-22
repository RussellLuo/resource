#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_exception_detail(e):
    if not isinstance(e, Exception):
        return u''
    return u'%s: %s' % (e.__class__.__name__, e.message)
