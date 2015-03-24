#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ## Default Domain Name
# scheme + domain + port
DOMAIN_NAME = ''


# ## Default Trailing Slash scheme
# When set to `True`, append a trailing slash mandatorily to every URLs.
# When set to `False`, remove the trailing slash mandatorily from every URLs.
TRAILING_SLASH = False


# ## Default Serializing scheme
# serialize data and bind it with type names
WITH_TYPE_NAME = False


# ## Default Date and time Format
# using UTC Format, see http://www.w3.org/TR/NOTE-datetime for details
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# ## Default item-size Per Page
PER_PAGE = 20


# ## Cross-Origin Options
CROSS_ORIGIN = False  # disabled
ACCESS_CONTROL_ALLOW_ORIGIN = '*'  # any domain
ACCESS_CONTROL_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
ACCESS_CONTROL_ALLOW_HEADERS = ['Content-Type']
ACCESS_CONTROL_MAX_AGE = 864000  # 10 days


# ## Default Authorizer Class
AUTH = 'rsrc.Auth'


# ## Default settings for token
SECRET_KEY = 'your-own-secret-key'
TOKEN_EXPIRES = 3600
TOKEN_USER = 'rsrc.contrib.token.TokenUser'


# ## Default settings for logger
LOGGER_ENABLED = False
LOGGER_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
LOGGER_LEVEL = 'DEBUG'
LOGGER_FORMAT = '%(asctime)s.%(msecs)03d %(name)-10s %(levelname)-8s %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
