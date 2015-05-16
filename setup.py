#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'testifi',
    'testifi.resources',
]

setup(
    name='testifi',
    version='1.0.0',
    description='Web-app for testing websites against certifi',
    author='Cory Benfield',
    author_email='cory@lukasa.co.uk',
    url='https://testifi.io/',
    packages=packages,
    package_dir={'testifi': 'testifi'},
    license='MIT License',
    entry_points={
        'console_scripts': [
            'testifi = testifi.server:runServer',
        ],
    },
)
