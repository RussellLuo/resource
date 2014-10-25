#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itsdangerous import (
    TimedJSONWebSignatureSerializer as TJWSSerializer,
    SignatureExpired, BadSignature
)


def make_token(secret_key, data, expires):
    s = TJWSSerializer(secret_key, expires_in=expires)
    token = s.dumps(data)
    return token


def load_data(secret_key, token):
    s = TJWSSerializer(secret_key)
    try:
        data = s.loads(token)
        return data
    except SignatureExpired:  # valid token, but expired
        return None
    except BadSignature:  # invalid token
        return None
