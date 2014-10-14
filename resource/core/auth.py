#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .exceptions import (
    MethodNotAllowedError, UnauthorizedError, ForbiddenError
)


class BasicAuth(object):

    allowed_methods = (
        'GET_LIST', 'GET_ITEM',
        'POST', 'PUT', 'PATCH', 'DELETE'
    )

    def check_auth(self, method, auth_params=None):
        if method not in self.allowed_methods:
            raise MethodNotAllowedError()

        if not self.authenticated(auth_params or {}):
            headers = {
                'WWW-Authenticate': 'Basic realm:"resource"'
            }
            raise UnauthorizedError(headers=headers)

        if not self.authorized():
            raise ForbiddenError()

    def authenticated(self, auth_params):
        """Authenticate credentials given by `auth_params`."""
        return False

    def authorized(self):
        """Validate if the authenticated user is allowed to pass through."""
        return False
