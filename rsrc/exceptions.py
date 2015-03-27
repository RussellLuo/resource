"""Handled exceptions raised by Resources.

Inspired by `Django REST framework` - https://github.com/tomchristie/django-rest-framework
"""
from __future__ import unicode_literals

from . import status


def get_exception_detail(e):
    if not isinstance(e, Exception):
        return u''
    return u'%s: %s' % (e.__class__.__name__, e.message)


class BaseError(Exception):
    """Base class for Resource exceptions."""
    pass


class StatusCodeError(BaseError):
    """
    Base class for kinds of Status-Code Resource exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ''

    def __init__(self, detail=None, headers=None):
        self.detail = detail or self.default_detail
        self.headers = headers

    def __str__(self):
        return self.detail


class BadRequestError(StatusCodeError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request.'


class UnauthorizedError(StatusCodeError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Unauthorized.'


class ForbiddenError(StatusCodeError):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Forbidden.'


class NotFoundError(StatusCodeError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'


class MethodNotAllowedError(StatusCodeError):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = 'Method not allowed.'
