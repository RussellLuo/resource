#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

description = 'A Python library concentrated on the Resource layer of RESTful APIs.'

install_requires = [
    'python-easyconfig>=0.1.0',
    'JsonForm>=0.0.2',
    'JsonSir>=0.0.2',
]

setup(
    name='Resource',
    version='0.2.1',
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
)
