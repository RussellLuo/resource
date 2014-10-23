#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from importlib import import_module

from . import default_settings as settings


# Override default settings if `RESOURCE_SETTINGS_MODULE` is given
custom_settings_module = os.environ.get('RESOURCE_SETTINGS_MODULE', None)
if custom_settings_module is not None:
    custom_settings = import_module(custom_settings_module)
    for attr_name in dir(custom_settings):
        if not attr_name.startswith('_'):
            attr_value = getattr(custom_settings, attr_name)
            setattr(settings, attr_name, attr_value)
