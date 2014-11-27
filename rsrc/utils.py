#!/usr/bin/env python
# -*- coding: utf-8 -*-


def import_object(name):
    """Imports an object by name.

    import_object('x') is equivalent to 'import x'.
    import_object('x.y.z') is equivalent to 'from x.y import z'.

    >>> import tornado.escape
    >>> import_object('tornado.escape') is tornado.escape
    True
    >>> import_object('tornado.escape.utf8') is tornado.escape.utf8
    True
    >>> import_object('tornado') is tornado
    True
    >>> import_object('tornado.missing_module')
    Traceback (most recent call last):
        ...
    ImportError: No module named missing_module

    Borrowed from `tornado` - https://github.com/tornadoweb/tornado
    """
    if name.count('.') == 0:
        return __import__(name, None, None)

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])


def normalize_uri(uri):
    """Normalize `uri` according to `settings.TRAILING_SLASH`.

    settings.TRAILING_SLASH | uri               | normalized
    ----------------------- | ----------------- | -----------------
    True                    | '/'               | '/'
    True                    | 'www.github.com'  | 'www.github.com/'
    True                    | 'www.github.com/' | 'www.github.com/'
    False                   | '/'               | '/'
    False                   | 'www.github.com'  | 'www.github.com'
    False                   | 'www.github.com/' | 'www.github.com'
    """
    from rsrc import settings
    normalized = uri.rstrip('/')
    if settings.TRAILING_SLASH:
        normalized = normalized + '/'
    return normalized or '/'
