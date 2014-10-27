#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TokenUser(object):
    """Handle the `token-key` of the user.

    `token-key` is token related data stored in user model.

    Below is a recommended implementation:

        token-key               | user model
        ----------------------- | ----------
        pk (primary key)        | id
        secret (JWT secret key) | jwt_secret

    Of course, you can build `token-key` with your preferred data.
    """
    @classmethod
    def get_key(cls, username, password):
        """Get token-key of the user that matches `username` and `password`.

        Should be overridden with custom logic.
        """
        return None

    @classmethod
    def exists(cls, key):
        """Check if `key` matches an existing user.

        Should be overridden with custom logic.
        """
        return False

    @classmethod
    def invalidate_key(cls, key):
        """Invalidate the given `key`.

        In recommended implementation, this means:
            Find an user that matches pk-part of `key`, and change his
            secret-part of `key`.

        Must be overridden with custom logic.
        """
        raise NotImplementedError()
