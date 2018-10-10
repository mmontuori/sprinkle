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
from clsync import exceptions
from clsync import operation
import json
import os

class ClSync:

    def __init__(self, config):
        logging.debug('constructing ClSync')
        if config is None:
            logging.error("configuration is None. Cannot continue!")
            raise Exception("None value for configuration")
        if config['rclone_workdir'] == None:
            logging.error("working directory is None. Cannot continue!")
            raise Exception("None value for working directory")
        if not common.is_dir(config['rclone_workdir']):
            logging.error("working directory " + str(config['rclone_workdir']) + " not found. Cannot continue!")
            raise Exception("Working directory " + config['rclone_workdir'] + " not found")
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

    def ls(self, file):
        logging.debug('lsjson of file: ' + file)
        json_ret = ''
        files = {}
        for remote in self.get_remotes():
            logging.debug('getting lsjson from ' + remote + file)
            try:
                json_out = self._rclone.lsjson(remote, file)
            except exceptions.FileNotFoundException as e:
                json_out = '[]'
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
                files[tmp_json_file['Path']] = tmp_file
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

    def index_local_dir(self, local_dir):
        clfiles = {}
        for root, dirs, files in os.walk(local_dir):
            for name in dirs:
                full_path = os.path.join(root, name)
                # logging.debug('adding ' + full_path + ' to list')
                tmp_clfile = clfile.ClFile()
                tmp_clfile.is_dir = True
                tmp_clfile.path = os.path.dirname(full_path)
                tmp_clfile.name = name
                tmp_clfile.size = "-1"
                tmp_clfile.mod_time = os.stat(full_path).st_mtime
                clfiles[tmp_clfile.path+'/'+tmp_clfile.name] = tmp_clfile
            for name in files:
                full_path = os.path.join(root, name)
                # logging.debug('adding ' + full_path + ' to list')
                tmp_clfile = clfile.ClFile()
                tmp_clfile.is_dir = False
                tmp_clfile.path = os.path.dirname(full_path)
                tmp_clfile.name = name
                tmp_clfile.size = os.stat(full_path).st_size
                tmp_clfile.mod_time = os.stat(full_path).st_mtime
                clfiles[tmp_clfile.path+'/'+tmp_clfile.name] = tmp_clfile
        logging.debug('retrieved ' + str(len(clfiles)) + ' files')
        return clfiles

    def compare_clfiles(self, local_dir, local_clfiles, remote_clfiles):
        logging.debug('comparing clfiles')
        logging.debug('local directory: ' + local_dir)
        logging.debug('local clfiles size: ' + str(len(local_clfiles)))
        logging.debug('remote clfiles size: ' + str(len(remote_clfiles)))
        operations = []
        for local_path in local_clfiles:
            local_clfile = local_clfiles[local_path]
            logging.debug('checking local clfile: ' + local_path + " name: " + local_clfile.name)
            rel_name = common.remove_localdir(local_dir, local_clfile.path)
            logging.debug('relative name: ' + rel_name)
            if local_path not in remote_clfiles:
                logging.debug('not found in remote_clfiles')
                local_clfile.remote_path = rel_name
                op = operation.Operation(operation.Operation.ADD,
                                         local_clfile, None)
                operations.append(op)
            # UPDATE operation
            # REMOVE operation
        return operations

    def backup(self, local_dir):
        logging.debug('backing up directory ' + local_dir)
        if not common.is_dir(local_dir):
            logging.error("local directory " + local_dir + " not found. Cannot continue!")
            raise Exception("Local directory " + local_dir + " not found")
        local_clfiles = self.index_local_dir(local_dir)
        remote_clfiles = self.ls(os.path.basename(local_dir))
        ops = self.compare_clfiles(local_dir, local_clfiles, remote_clfiles)
        for op in ops:
            logging.debug('operation: ' + op.operation + ", path: " + op.src.path + ', ' +
                          op.src.remote_path)
            if op.src.is_dir:
                logging.debug('skipping directory ' + op.src.path)
                continue
            best_remote = self.get_best_remote(int(op.src.size))
            logging.debug('best remote: ' + best_remote)
            self.copy(op.src.path+'/'+op.src.name, op.src.remote_path, best_remote)

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

    def copy(self, src, dst, remote):
        logging.debug('copy ' + src + ' to ' + remote + dst)
        self._rclone.copy(src, remote+dst)

    def move(self, src, dst):
        logging.debug('move ' + src + ' to ' + dst)

    def sync(self, path):
        logging.debug('synchronize path ' + path)

