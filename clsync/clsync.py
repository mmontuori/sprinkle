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

    def get_size(self):
        logging.debug('getting total size')
        total_size = 0
        for remote in self.get_remotes():
            size = self._rclone.get_size(remote)
            logging.debug('size of ' + remote + ' is ' + str(size))
            total_size += size
        return total_size

    def get_free(self):
        logging.debug('getting total free size')
        total_size = 0
        for remote in self.get_remotes():
            size = self._rclone.get_free(remote)
            logging.debug('free of ' + remote + ' is ' + str(size))
            total_size += size
        return total_size

    def get_max_file_size(self):
        logging.debug('getting total maximum file size')
        total_size = 0
        for remote in self.get_remotes():
            size = self._rclone.get_free(remote)
            logging.debug('free of ' + remote + ' is ' + str(size))
            if size > total_size:
                total_size = size
        return total_size

    def get_best_remote(self, requested_size=1):
        logging.debug('selecting best remote with the most available space to store size: ' + str(requested_size))
        best_remote = None
        highest_size = 0
        for remote in self.get_remotes():
            size = self._rclone.get_free(remote)
            logging.debug('free of ' + remote + ' is ' + str(size))
            if size > highest_size:
                if requested_size <= size:
                    highest_size = size
                    best_remote = remote
        return best_remote

