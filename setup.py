#!/usr/bin/env python
"""
setup.py PuPI setup project file
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
__revision__ = "1"

from setuptools import setup
from setuptools import find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='sprinkle',
    version='0.1.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #packages=['sprinkle'],
    url='https://gitlab.com/mmontuori/sprinkle',
    license='',
    author='mmontuori',
    author_email='michael.montuori@gmail.com',
    description='Sprinkle and backup files in the cloud across multiple storage',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
