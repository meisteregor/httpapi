#!/usr/bin/env python3
# -*- coding: UTF-8

""" Setup script """

from setuptools import setup, find_packages


setup(
    # Metadata
    name='http_api',
    version='1.0',
    description='httpsearchapi',
    maintainer='egormeister',
    maintainer_email='meisteregor@yandex.ru',
    platforms=['POSIX'],
    # Python packages
    packages=find_packages(),
    install_requires=[
        'flask',
        'gevent~=1.2.2',
    ],
    # __main__ module
    data_files=[['', ['__main__.py']]]
)
