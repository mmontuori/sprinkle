#!/usr/bin/env python
"""
operation wrapper class

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

from clsync import clfile

class Operation(object):

    ADD = "add"
    UPDATE = "update"
    REMOVE = ""

    def __init__(self, operation, src, dst):
        if operation.lower() != 'add' and operation.lower() != 'update' and operation.lower() != 'remove':
            raise Exception('invalid operation: ' + operation)
        self.operation = operation
        self.src = src
        self.dst = dst

