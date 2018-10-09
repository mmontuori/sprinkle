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
from clsync import rclone
from clsync import common
from clsync import clfile
import json

class ClSync:

    def __init__(self, config):
        logging.debug('constructing ClSync')
        if config is None:
            logging.error("configuration is None. Cannot continue!")
            raise Exception("None value for configuration")
        self._config = config
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
        files = []
        for remote in self.get_remotes():
            logging.debug('getting lsjson from ' + remote + file)
            json_out = self._rclone.lsjson(remote, file)
            tmp_json = json.loads(json_out)
            for tmp_json_file in tmp_json:
                tmp_file = clfile.ClFile()
                logging.debug('path: ' + tmp_json_file['Path'])
                tmp_file.remote = remote
                tmp_file.path = tmp_json_file['Path']
                tmp_file.name = tmp_json_file['Name']
                tmp_file.size = tmp_json_file['Size']
                tmp_file.mime_type = tmp_json_file['MimeType']
                tmp_file.mod_time = tmp_json_file['ModTime']
                tmp_file.is_dir = tmp_json_file['IsDir']
                tmp_file.id = tmp_json_file['ID']
                files.append(tmp_file)
                json_ret = json_ret + '||' + json_out
                #logging.debug('json_ret: ' + json_ret)
        return files

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

    def rmdir(self, directory):
        logging.debug('removing directory ' + directory)

    def get_version(self):
        logging.debug('getting version')

    def touch(self, file):
        logging.debug('touching file ' + file)

    def delete_file(self, file):
        logging.debug('deleting file ' + file)

    def delete(self, path):
        logging.debug('deleting path ' + path)

    def copy(self, src, dst):
        logging.debug('copy ' + src + ' to ' + dst)

    def move(self, src, dst):
        logging.debug('move ' + src + ' to ' + dst)

    def sync(self, path):
        logging.debug('synchronize path ' + path)

