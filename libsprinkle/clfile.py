#!/usr/bin/env python3
"""
container class for a file
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "1.0"
__revision__ = "1"

class ClFile(object):

    remote = None
    path = None
    remote_path = None
    name = None
    size = None
    mime_type = None
    mod_time = None
    is_dir = None
    id = None
