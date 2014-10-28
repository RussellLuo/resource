#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TokenUser(object):
    """Handle the `token-key` of the user.

    `token-key` is token (JWT) related data stored in user model.

    Below is the structure of `token-key`:

        token-key               | user model
        ----------------------- | ----------
        pk (primary key)        | id
        secret (JWT secret key) | jwt_secret

    `jwt_secret` is a recommended column name. Of course, you can use your
    preferred name.
    """
    @classmethod
    def get_key(cls, username, password):
        """Get token-key of the user that matches `username` and `password`.

        Must return a tuple (pk, secret).

        Should be overridden with custom logic.
        """
        return None, None

    @classmethod
    def exists(cls, pk, secret):
        """Check if `pk` and `secret` match an existing user.

        Should be overridden with custom logic.
        """
        return False

    @classmethod
    def invalidate_key(cls, pk):
        """Invalidate the key related to `pk`.

        In recommended implementation, this means:
            + Find an user that matches `pk` as his `id`, and change his
            `jwt_secret`, and return True.
            + If `pk` matches no user, return False

        Should be overridden with custom logic.
        """
        return False
