#!/usr/bin/env python3
"""
operation wrapper class
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "2"

from libsprinkle import clfile

class Operation(object):

    ADD = "add"
    UPDATE = "update"
    REMOVE = "remove"

    def __init__(self, operation, src, dst):
        if operation.lower() != 'add' and operation.lower() != 'update' and operation.lower() != 'remove':
            raise Exception('invalid operation: ' + operation)
        self.operation = operation
        self.src = src
        self.dst = dst

