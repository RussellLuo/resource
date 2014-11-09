#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ## Default Domain Name
# scheme + domain + port
DOMAIN_NAME = ''


# ## Default Date and time Format
# using UTC Format, see http://www.w3.org/TR/NOTE-datetime for details
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


# ## Default item-size Per Page
PER_PAGE = 20


# ## Default Authorizer Class
AUTH = 'resource.BasicAuth'


# ## Default settings for token
SECRET_KEY = 'your-own-secret-key'
TOKEN_EXPIRES = 3600
TOKEN_USER = 'resource.contrib.token.TokenUser'
