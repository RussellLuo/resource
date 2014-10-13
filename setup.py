#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

description = 'A library concentrated on the Resource layer of RESTful API.'

install_requires = [
    'jsonpatch==1.7',
    'pymongo==2.7.2',
    'SQLAlchemy==0.9.7',
    'requests==2.4.1',
    'Flask==0.10.1',
    'mkdocs==0.9',
]

dependency_links = [
    'git+https://github.com/RussellLuo/jsonform.git#egg=jsonform',
    'git+https://github.com/RussellLuo/py-mongosql.git#egg=py-mongosql',
]

setup(
    name='resource',
    version='0.0.1',
    author='RussellLuo',
    author_email='luopeng.he@gmail.com',
    description=description,
    license='MIT',
    long_description=description,
    packages=['resource'],
    url='https://github.com/RussellLuo/resource',
    install_requires=install_requires,
    dependency_links=dependency_links,
)
