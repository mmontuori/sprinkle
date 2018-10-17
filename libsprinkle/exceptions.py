#!/usr/bin/env python3
"""
custom file not found exception
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "2"

class FileNotFoundException(Exception):

    def __init__(self, message):
        self.message = message
