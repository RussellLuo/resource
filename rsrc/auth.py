#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .exceptions import (
    MethodNotAllowedError, UnauthorizedError, ForbiddenError
)


class BasicAuth(object):
    """Basic Authentication."""

    # inherent limit of the resource
    allowed_methods = (
        'GET_LIST', 'GET_ITEM',
        'POST', 'PUT', 'PATCH', 'DELETE'
    )

    def check_auth(self, method, auth_params=None):
        if method not in self.allowed_methods:
            raise MethodNotAllowedError()

        auth_params = auth_params or {}
        if not self.authenticated(method, auth_params):
            headers = {
                'WWW-Authenticate': 'Basic realm:"resource"'
            }
            raise UnauthorizedError(headers=headers)

        if not self.authorized():
            raise ForbiddenError()

    def authenticated(self, method, auth_params):
        """Authenticate the user with credentials in `auth_params`.

        Sometimes, `method` also affect the authentication here.
        """
        return False

    def authorized(self):
        """Validate if the authenticated user has required permissions."""
        return True
