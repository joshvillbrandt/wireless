#!/usr/bin/env python

from setuptools import setup

setup(
    name='wireless',
    version='0.1.0',
    description='A dead simple, cross-platform Python library to connect to ' +
    'wireless networks.',
    long_description=open('README.md').read(),
    url='https://github.com/joshvillbrandt/wireless',
    author='Josh Villbrandt',
    author_email='josh@javconcepts.com',
    license=open('LICENSE').read(),
    packages=['wireless'],
    setup_requires=[
        'tox',
        'nose',
        'flake8'
    ],
    install_requires=[
    ],
    scripts=[],
    test_suite='tests',
    zip_safe=False
)
