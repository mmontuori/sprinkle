#!/usr/bin/env python
"""
custom file not found exception

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

class FileNotFoundException(Exception):

    def __init__(self, message):
        self.message = message
