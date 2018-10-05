#!/usr/bin/env python
"""
clustersync main module

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

import logging
import os.path
from mmontuori import config

class ClSync:

    def __init__(self, config_file):
        logging.debug('constructing ClSync')
        if config_file == None:
            logging.error("configuration file " + str(config_file) + " is None. Cannot continue!")
            raise Exception("None value for configuration file")
        if not os.path.isfile(config_file):
            logging.error("configuration file " + str(config_file) + " not found. Cannot continue!")
            raise Exception("Configuration file not found")