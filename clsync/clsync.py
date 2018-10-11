#!/usr/bin/env python
"""
clustersync main module
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"

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
        if 'distribution_type' in config:
            self._distribution_type = config['distribution_type']
        else:
            self._distribution_type = 'mas'
        if self._distribution_type == 'mas':
            self._cached_free = {}
        if 'compare_method' in config:
            self._compare_method = config['compare_method']
        else:
            self._compare_method = 'size'
        self._remotes = None
        self._remote_calls = 0

    def get_remotes(self):
        logging.debug('getting rclone remotes')
        if self._remotes is None or self._remote_calls > 100:
            self._remotes = self._rclone.get_remotes()
            self._remote_calls = 0
        self._remote_calls += 1
        return self._remotes

    def mkdir(self, directory):
        logging.debug('makind directory ' + directory)
        for remote in self.get_remotes():
            logging.debug('creating directory ' + remote + directory)
            self._rclone.mkdir(remote, directory)

    def ls(self, file):
        logging.debug('lsjson of file: ' + file)
        if not file.startswith('/'):
            file = '/' + file
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
                #logging.debug('path: ' + file + '/' + tmp_json_file['Path'])
                tmp_file.remote = remote
                tmp_file.path = file + '/' + tmp_json_file['Path']
                tmp_file.name = tmp_json_file['Name']
                tmp_file.size = tmp_json_file['Size']
                tmp_file.mime_type = tmp_json_file['MimeType']
                tmp_file.mod_time = tmp_json_file['ModTime']
                tmp_file.is_dir = tmp_json_file['IsDir']
                tmp_file.id = tmp_json_file['ID']
                files[file + '/' + tmp_json_file['Path']] = tmp_file
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
        if self._distribution_type == 'mas':
            logging.debug('selecting best remote with the most available space to store size: ' + str(requested_size))
            best_remote = None
            highest_size = 0
            size = 0
            for remote in self.get_remotes():
                if remote not in self._cached_free:
                    size = self._rclone.get_free(remote)
                    self._cached_free[remote] = size
                else:
                    size = self._cached_free[remote]
                logging.debug('free of ' + remote + ' is ' + str(size))
                if size > highest_size:
                    if requested_size <= size:
                        highest_size = size
                        best_remote = remote
            self._cached_free[best_remote] = highest_size - requested_size
            return best_remote
        else:
            logging.error('distribution mode ' + self._distribution_type + ' not supported.')
            raise Exception('unsupported distribution mode ' + self._distribution_type)

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
                clfiles[common.normalize_path(tmp_clfile.path+'/'+tmp_clfile.name)] = tmp_clfile
            for name in files:
                full_path = os.path.join(root, name)
                # logging.debug('adding ' + full_path + ' to list')
                tmp_clfile = clfile.ClFile()
                tmp_clfile.is_dir = False
                tmp_clfile.path = os.path.dirname(full_path)
                tmp_clfile.name = name
                tmp_clfile.size = os.stat(full_path).st_size
                tmp_clfile.mod_time = os.stat(full_path).st_mtime
                clfiles[common.normalize_path(tmp_clfile.path+'/'+tmp_clfile.name)] = tmp_clfile
        logging.debug('retrieved ' + str(len(clfiles)) + ' files')
        return clfiles

    def compare_clfiles(self, local_dir, local_clfiles, remote_clfiles):
        logging.debug('comparing clfiles')
        logging.debug('local directory: ' + local_dir)
        logging.debug('local clfiles size: ' + str(len(local_clfiles)))
        logging.debug('remote clfiles size: ' + str(len(remote_clfiles)))
        remote_dir = os.path.dirname(local_dir)
        operations = []
        for local_path in local_clfiles:
            local_clfile = local_clfiles[local_path]
            if local_clfile.is_dir:
                continue
            logging.debug('checking local clfile: ' + local_path + " name: " + local_clfile.name)
            rel_name = common.remove_localdir(local_dir, local_clfile.path+'/'+local_clfile.name)
            rel_path = common.remove_localdir(local_dir, local_clfile.path)
            logging.debug('relative name: ' + rel_name)
            if rel_name not in remote_clfiles:
                logging.debug('not found in remote_clfiles')
                local_clfile.remote_path = rel_path
                op = operation.Operation(operation.Operation.ADD,
                                         local_clfile, None)
                operations.append(op)
            else:
                logging.debug('file found in remote_clfiles')
                remote_clfile = remote_clfiles[rel_name]
                if self._compare_method == 'size':
                    size_local = local_clfile.size
                    size_remote = remote_clfile.size
                    current_remote = remote_clfiles[rel_name].remote
                    logging.debug('local_file.size:' + str(local_clfile.size) +
                                  ', remote_clfile.size:' + str(remote_clfile.size))
                    if size_local != size_remote:
                        logging.debug('file has changed')
                        local_clfile.remote_path = rel_path
                        local_clfile.remote = current_remote
                        op = operation.Operation(operation.Operation.UPDATE,
                                                 local_clfile, None)
                        operations.append(op)
                else:
                    logging.error('compare_method: ' + self._compare_method + ' not valid!')
                    raise Exception('compare_method: ' + self._compare_method + ' not valid!')

        for remote_path in remote_clfiles:
            remote_clfile = remote_clfiles[remote_path]
            logging.debug('checking file ' + remote_dir+remote_path + ' for deletion')
            if remote_dir+remote_path not in local_clfiles:
                logging.debug('file ' + remote_path + ' has been deleted')
                remote_clfile.remote_path = rel_path
                op = operation.Operation(operation.Operation.REMOVE,
                                         remote_clfile, None)
                operations.append(op)

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
            logging.debug('operation: ' + op.operation + ", path: " + op.src.path)
            if op.src.is_dir:
                logging.debug('skipping directory ' + op.src.path)
                continue
            if op.operation == operation.Operation.ADD:
                best_remote = self.get_best_remote(int(op.src.size))
                logging.debug('best remote: ' + best_remote)
                self.copy(op.src.path+'/'+op.src.name, op.src.remote_path, best_remote)
            if op.operation == operation.Operation.UPDATE:
                best_remote = self.get_best_remote(int(op.src.size))
                logging.debug('best remote: ' + best_remote)
                self.copy(op.src.path + '/' + op.src.name, op.src.remote_path, op.src.remote)
            if op.operation == operation.Operation.REMOVE:
                self.delete_file(op.src.path, op.src.remote)

    def rmdir(self, directory):
        logging.debug('removing directory ' + directory)

    def get_version(self):
        logging.debug('getting version')

    def touch(self, file):
        logging.debug('touching file ' + file)

    def delete_file(self, file, remote):
        logging.debug('deleting file ' + remote+file)
        self._rclone.delete_file(remote, file)

    def delete(self, path):
        logging.debug('deleting path ' + path)

    def copy(self, src, dst, remote):
        logging.debug('copy ' + src + ' to ' + remote + dst)
        self._rclone.copy(src, remote+dst)

    def move(self, src, dst):
        logging.debug('move ' + src + ' to ' + dst)

    def sync(self, path):
        logging.debug('synchronize path ' + path)

