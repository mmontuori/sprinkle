#!/usr/bin/env python3
"""
config.py: configuration module responsible for loading configuration and rules
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2018, Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__licemse__ = "GPLv3"
__version__ = "1.0"
__revision__ = "1"
__maintainer__ = "Michael Montuori [michael.montuori@gmail.com]"

try:
    import ConfigParser
except:
    import configparser
import os.path
try:
    import StringIO
except:
    from io import StringIO
import logging

class Config(object):
    """The Config class is responsible for reading configuration file and rules file
    including defaults where possible.
    """

    _conf_obj = None

    _CONFIG_MAIN_SECTION = 'MAIN'


    def __init__(self, config_file):
        """initialization, the parameter config_file and rule_file are read
        and variables are populated"""
        self._config_file = config_file
        self.load_config()

    def load_config(self):
        """function responsible for loading the actual configuration file from config_file.
        load_config also handles defaults where possible."""
        logging.debug('loading configuration from ' + self._config_file + '...')
        if not os.path.isfile(self._config_file):
            logging.error("File " + self._config_file + " not found")
            raise Exception("File " + self._config_file + " not found")
        else:
            config_str = '[' + self._CONFIG_MAIN_SECTION + ']\n' + open(self._config_file, 'r').read()
            try:
                config_fp = StringIO.StringIO(config_str)
            except:
                config_fp = StringIO(config_str)
            try:
                self._conf_obj = ConfigParser.RawConfigParser()
            except:
                self._conf_obj = configparser.RawConfigParser()
            self._conf_obj.readfp(config_fp)

    def get_config(self):
        retconf = {}
        for name, value in self._conf_obj.items(self._CONFIG_MAIN_SECTION):
            retconf[name] = value
        return retconf