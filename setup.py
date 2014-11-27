#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

description = 'A Python library concentrated on the Resource layer of RESTful APIs.'

install_requires = [
    'jsonpatch==1.7',
    'pymongo==2.7.2',
    'SQLAlchemy==0.9.7',
    'jsonform==0.0.1',
    'jsonsir==0.0.1',
    'mongosql<=1.2.2',
]

dependency_links = [
    'https://github.com/RussellLuo/jsonform/archive/master.zip#egg=jsonform-0.0.1',
    'https://github.com/RussellLuo/jsonsir/archive/master.zip#egg=jsonsir-0.0.1',
    'https://github.com/RussellLuo/py-mongosql/archive/master.zip#egg=mongosql-1.2.2',
]

setup(
    name='Resource',
    version='0.1.3',
    author='RussellLuo',
    author_email='luopeng.he@gmail.com',
    maintainer='RussellLuo',
    maintainer_email='luopeng.he@gmail.com',
    keywords='Resource, REST, Python',
    description=description,
    license='MIT',
    long_description=description,
    packages=find_packages(),
    url='https://github.com/RussellLuo/resource',
    install_requires=install_requires,
    dependency_links=dependency_links,
)
