"""Handled exceptions raised by Resources.

Inspired by `Django REST framework` - https://github.com/tomchristie/django-rest-framework
"""
from __future__ import unicode_literals

from . import status


class RSRCException(Exception):
    """
    Base class for Resource exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ''

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

    def __str__(self):
        return self.detail


class NotFound(RSRCException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
