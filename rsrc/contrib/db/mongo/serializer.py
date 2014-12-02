#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rsrc import settings
from jsonsir import Serializer
from jsonsir.contrib.intencoder import IntEncoder
from jsonsir.contrib.boolencoder import BoolEncoder
from jsonsir.contrib.regexencoder import RegexEncoder
from jsonsir.contrib.objectidencoder import ObjectIdEncoder
from jsonsir.contrib.datetimeencoder import DateTimeEncoder


# instantiate `Serializer` (bound with specified encoders)
serializer = Serializer([
    IntEncoder(),
    BoolEncoder(),
    RegexEncoder(),
    ObjectIdEncoder(),
    DateTimeEncoder(settings.DATE_FORMAT),
])
