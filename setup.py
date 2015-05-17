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
    install_requires=[
        'Twisted>=15.1.0',
        'pyOpenSSL>=0.15.1',
        'service-identity>=14.0.0',
        'structlog>=15.1.0',
        'treq>=15.0.0',
        'requests>=2.7.0',
    ],
    entry_points={
        'console_scripts': [
            'testifi = testifi.server:runServer',
            'certifi-test = testifi.certifi_test:main'
        ],
    },
)
