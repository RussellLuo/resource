#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='resource',
    version='0.0.1',
    author='RussellLuo',
    author_email='luopeng.he@gmail.com',
    description='A library concentrated on the Resource layer of RESTful API.',
    license='MIT',
    long_description=long_description,
    packages=['resource'],
    url='https://github.com/RussellLuo/resource',
    install_requires=['jsonschema', 'jsonform', 'jsonpatch',
                      'pymongo', 'flask'],
)
