#!/usr/bin/env python
# -*- coding: utf-8 -*-

from resource import settings, View, Response, status

from .signer import make_token


class TokenView(View):
    """Generate tokens based on uesrname and password.

    Login in RESTful API:

        1. POST (with username and password) to generate a token

            $ curl -X POST -H "Content-Type: application/json" -d '{"username":"russell","password":"123456"}' http://localhost/api/tokens/

        2. get the token from the response (in JSON format) of POST

            {"token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQxNDIyNDExOSwiaWF0IjoxNDE0MjIwNTE5fQ.eyJwayI6IjU0NGI0YWRhMWQ0MWM4MzExMjRhNDBjZCJ9.d_6Oi4ePS7z9NhK9b9J23H3KQx4u_EdzT-VHDnV2fC8", "expires": 3600}

        If `username` or `password` is invalid, you will get:

            {"token": null, "expires": 0}

        3. use `TokenAuth` to protect your resources at server side,
        and the client should set the token as username part in the
        Authorization header to access resources

            $ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQxNDIyNDExOSwiaWF0IjoxNDE0MjIwNTE5fQ.eyJwayI6IjU0NGI0YWRhMWQ0MWM4MzExMjRhNDBjZCJ9.d_6Oi4ePS7z9NhK9b9J23H3KQx4u_EdzT-VHDnV2fC8:unused -i -X GET http://localhost/api/resource/

        4. for browser users, save the token in cookies of their browsers,
        and get the token from cookies to set Authorization header every time
    """

    def post(self, data):
        username = data.get('username')
        password = data.get('password')
        expires = data.get('expires')
        if expires is None:
            expires = settings.TOKEN_EXPIRES

        user_pk = self.get_user_pk(username, password)
        if user_pk is None:
            token = None
            expires = 0
        else:
            token = make_token(settings.SECRET_KEY, {'pk': user_pk}, expires)

        return Response({'token': token, 'expires': expires},
                        status=status.HTTP_201_CREATED)

    def get_user_pk(self, username, password):
        """Get the `pk` of user which matches `username` and `password`.

        Should be overridden with custom logic.
        """
        return None
