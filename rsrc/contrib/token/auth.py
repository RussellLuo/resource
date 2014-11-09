#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rsrc import settings, BasicAuth
from rsrc.utils import import_object

from .signer import load_data


class TokenAuth(BasicAuth):
    """Token-based authentication.

    The Authorization header will contain the auth token as the username.
    """

    token_user = import_object(settings.TOKEN_USER)

    def authenticated(self, method, auth_params):
        token = auth_params.get('username')
        if token is None:
            return False

        data = load_data(settings.SECRET_KEY, token)
        if data is None:
            return False

        return self.token_user.exists(**data)
