#!/usr/bin/env python
"""
setup.py PuPI setup project file
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "1"

import os
from setuptools import setup
from setuptools import find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

this = os.path.dirname(os.path.realpath(__file__))

def read(name):
    with open(os.path.join(this, name)) as f:
        return f.read()

setup(
    name='sprinkle-py',
    version='0.1.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #packages=['sprinkle'],
    #install_requires=read('requirements.txt'),
    url='https://gitlab.com/mmontuori/sprinkle',
    license='GPLv3',
    include_package_data=True,
    author='mmontuori',
    author_email='michael.montuori@gmail.com',
    description='Sprinkle is a volume clustering utility based on [RClone](https://rclone.org).',
    long_description=long_description,
    keywords='sprinkle cloud backup restore',
    zip_safe=True,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English'
    ],
    scripts=['sprinkle.py']
)
