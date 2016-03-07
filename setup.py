#!/usr/bin/env python

from setuptools import setup

# auto-convert README.md
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (ImportError, OSError):
    # we'll just use the poorly formatted Markdown file instead
    long_description = open('README.md').read()

setup(
    name='wireless',
    version='0.3.2',
    description='A dead simple, cross-platform Python library to connect to ' +
    'wireless networks.',
    long_description=long_description,
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
