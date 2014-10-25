#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import settings, BasicAuth

from .signer import load_data


class TokenAuth(BasicAuth):
    """Token-based authentication.

    The Authorization header will contain the auth token as the username.
    """
    def authenticated(self, method, auth_params):
        token = auth_params.get('username')
        if token is None:
            return False

        data = load_data(settings.SECRET_KEY, token)
        if data is None:
            return False

        return self.has_user(data['pk'])

    def has_user(self, user_pk):
        """Check if `user_pk` matches an existing user.

        Should be overridden with custom logic.
        """
        return False
