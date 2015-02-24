#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from .conf import settings


if settings.LOGGER_ENABLED:
    logging.basicConfig(
        level=settings.LOGGER_LEVEL,
        format=settings.LOGGER_FORMAT,
        datefmt=settings.LOGGER_DATE_FORMAT
    )

logger = logging.getLogger('rsrc')
