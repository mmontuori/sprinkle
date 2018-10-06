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
from clsync import rclone
import json
from clsync import common

class ClSync:

    def __init__(self, config_file):
        logging.debug('constructing ClSync')
        if config_file == None:
            logging.error("configuration file " + str(config_file) + " is None. Cannot continue!")
            raise Exception("None value for configuration file")
        if not os.path.isfile(config_file):
            logging.error("configuration file " + str(config_file) + " not found. Cannot continue!")
            raise Exception("Configuration file not found")
        conf = config.Config(config_file)
        self._config = conf.get_config()
        self._rclone = rclone.RClone(self._config['rclone_config'], self._config['rclone_exe'])

    def get_remotes(self):
        logging.debug('getting rclone remotes')
        return self._rclone.get_remotes()

    def mkdir(self, directory):
        logging.debug('makind directory ' + directory)
        for remote in self.get_remotes():
            logging.debug('creating directory ' + remote + directory)
            self._rclone.mkdir(remote, directory)

    def lsjson(self, file):
        logging.debug('lsjson of file: ' + file)
        json_ret = ''
        for remote in self.get_remotes():
            logging.debug('getting lsjson from ' + remote + file)
            json_out = self._rclone.lsjson(remote, file)
            json_ret = json_ret + '||' + json_out
            #logging.debug('json_ret: ' + json_ret)
        return common.combine_jsons(json_ret)

