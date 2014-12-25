#!/usr/bin/env python
# -*- coding: utf-8 -*-

from easyconfig import Config, envvar_object

from . import default_settings


settings = Config()
settings.from_object(default_settings)

# Override default settings if `RESOURCE_SETTINGS_MODULE` is given
settings.from_object(envvar_object('RESOURCE_SETTINGS_MODULE', True))
