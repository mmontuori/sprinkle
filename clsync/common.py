#!/usr/bin/env python
"""
common utilities

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

def combine_jsons(json_str):
    return '[' + json_str.replace(']\n',',',json_str.count(']\n')-1).replace('||[\n','')