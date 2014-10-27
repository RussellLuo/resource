#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import settings, View, Response, status
from resource.utils import import_object

from .signer import make_token


class TokenView(View):
    """Generate tokens based on uesrname and password.

    `Login` in RESTful API:
        1. POST (with username and password) to generate a token
        2. get the token from the response (in JSON format) of POST
        3. use `TokenAuth` to protect your resources at server side,
        and the client should set the token as username part in the
        Authorization header to access resources
        4. for browser users, save the token in cookies of their browsers,
        and get the token from cookies to set Authorization header every time
    """

    token_user = import_object(settings.TOKEN_USER)

    def post(self, data):
        username = data.get('username')
        password = data.get('password')
        expires = data.get('expires')
        if expires is None:
            expires = settings.TOKEN_EXPIRES

        key = self.token_user.get_key(username, password)
        if key is None:
            token = None
            expires = 0
        else:
            token = make_token(settings.SECRET_KEY, {'key': key}, expires)

        return Response({'token': token, 'expires': expires},
                        status=status.HTTP_201_CREATED)
