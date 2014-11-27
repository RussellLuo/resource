#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ## Default Domain Name
# scheme + domain + port
DOMAIN_NAME = ''


# ## Default Trailing Slash scheme
# When set to `True`, append a trailing slash mandatorily to every URLs.
# When set to `False`, remove the trailing slash mandatorily from every URLs.
TRAILING_SLASH = True


# ## Default Serializing scheme
# serialize data and bind it with type names
WITH_TYPE_NAME = False


# ## Default Date and time Format
# using UTC Format, see http://www.w3.org/TR/NOTE-datetime for details
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# ## Default item-size Per Page
PER_PAGE = 20


# ## Default Authorizer Class
AUTH = 'rsrc.BasicAuth'


# ## Default settings for token
SECRET_KEY = 'your-own-secret-key'
TOKEN_EXPIRES = 3600
TOKEN_USER = 'rsrc.contrib.token.TokenUser'
