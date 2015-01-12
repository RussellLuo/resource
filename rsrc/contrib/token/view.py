#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rsrc import settings, View, Response, status
from rsrc.exceptions import NotFoundError
from rsrc.utils import import_object

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

    def post(self, request):
        """Make a token based on `uesrname`, `password` and `expires`.
        """
        data = request.data

        username = data.get('username')
        password = data.get('password')

        # `expires` is optional
        expires = data.get('expires')
        if expires is None:
            expires = settings.TOKEN_EXPIRES

        pk, secret = self.token_user.get_key(username, password)
        if pk is None or secret is None:
            errors = {'errors': 'username or password is wrong'}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        token_data = {'pk': pk, 'secret': secret}
        token = make_token(settings.SECRET_KEY, token_data, expires)

        return Response({'id': pk, 'token': token, 'expires': expires},
                        status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Invalidate the token related to the user matches `pk`."""
        ok = self.token_user.invalidate_key(pk)
        if not ok:
            raise NotFoundError()

        return Response(status=status.HTTP_204_NO_CONTENT)
