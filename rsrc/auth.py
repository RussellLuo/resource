#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .exceptions import (
    MethodNotAllowedError, UnauthorizedError, ForbiddenError
)


class Auth(object):
    """The base class of Authentication."""

    def check_auth(self, method, auth_params=None):
        pass


class BasicAuth(Auth):
    """Basic Authentication."""

    # inherent limit of the resource
    allowed_methods = (
        'GET_LIST', 'GET_ITEM',
        'POST', 'PUT', 'PATCH',
        'DELETE_LIST', 'DELETE_ITEM'
    )

    def check_auth(self, method, auth_params=None):
        if method not in self.allowed_methods:
            raise MethodNotAllowedError()

        auth_params = auth_params or {}
        if not self.authenticated(method, auth_params):
            raise UnauthorizedError(headers=self.make_headers())

        if not self.authorized():
            raise ForbiddenError()

    def make_headers(self):
        """The response headers when authentication fails."""
        return {'WWW-Authenticate': 'Basic realm:"resource"'}

    def authenticated(self, method, auth_params):
        """Authenticate the user with credentials in `auth_params`.

        Sometimes, `method` also affect the authentication here.
        """
        return False

    def authorized(self):
        """Validate if the authenticated user has required permissions."""
        return True
