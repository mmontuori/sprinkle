#!/usr/bin/env python3
"""
clsync module
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "2"

import logging
from libsprinkle import rclone
from libsprinkle import common
from libsprinkle import clfile
from libsprinkle import exceptions
from libsprinkle import operation
import json
import os

class ClSync:

    def __init__(self, config):
        logging.debug('constructing ClSync')
        if config is None:
            logging.error("configuration is None. Cannot continue!")
            raise Exception("None value for configuration")
        if 'rclone_workdir' in config and config['rclone_workdir'] == None and not common.is_dir(config['rclone_workdir']):
            logging.error("working directory " + str(config['rclone_workdir']) + " not found. Cannot continue!")
            raise Exception("Working directory " + config['rclone_workdir'] + " not found")
        self._config = config
        if 'rclone_config' in self._config:
            rclone_config = self._config['rclone_config']
        else:
            rclone_config = None
        if 'rclone_exe' not in self._config:
            self._rclone = rclone.RClone(rclone_config)
        else:
            self._rclone = rclone.RClone(rclone_config, self._config['rclone_exe'])
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
        self._sizes = None
        self._frees = None

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
                json_out = self._rclone.lsjson(remote, file, ['--recursive'], True)
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

    def get_sizes(self):
        logging.debug('getting sizes')
        if self._sizes is None:
            self._sizes = {}
            for remote in self.get_remotes():
                size = self._rclone.get_size(remote)
                logging.debug('size of ' + remote + ' is ' + str(size))
                self._sizes[remote] = size
        return self._sizes

    def get_size(self):
        logging.debug('getting sizes')
        total_size = 0
        for remote in self.get_remotes():
            if self._sizes is None:
                size = self._rclone.get_size(remote)
            else:
                size = self._sizes[remote]
            logging.debug('size of ' + remote + ' is ' + str(size))
            total_size += size
        return total_size

    def get_frees(self):
        logging.debug('getting free sizes')
        if self._frees is None:
            self._frees = {}
            for remote in self.get_remotes():
                size = self._rclone.get_free(remote)
                logging.debug('free of ' + remote + ' is ' + str(size))
                self._frees[remote] = size
        return self._frees

    def get_free(self):
        logging.debug('getting total free size')
        total_size = 0
        for remote in self.get_remotes():
            if self._frees is None:
                size = self._rclone.get_free(remote)
            else:
                size = self._frees[remote]
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
            if op.src.is_dir and op.operation != operation.Operation.REMOVE:
                logging.debug('skipping directory ' + op.src.path)
                continue
            if op.operation == operation.Operation.ADD:
                best_remote = self.get_best_remote(int(op.src.size))
                logging.debug('best remote: ' + best_remote)
                common.print_line('backing up file ' + op.src.path+'/'+op.src.name +
                                  ' -> ' + best_remote+':'+op.src.remote_path)
                self.copy(op.src.path+'/'+op.src.name, op.src.remote_path, best_remote)
            if op.operation == operation.Operation.UPDATE:
                best_remote = self.get_best_remote(int(op.src.size))
                logging.debug('best remote: ' + best_remote)
                common.print_line('backing up file ' + op.src.path + '/' + op.src.name +
                                  ' -> ' + op.src.remote + ':' + op.src.remote_path)
                self.copy(op.src.path + '/' + op.src.name, op.src.remote_path, op.src.remote)
            if op.operation == operation.Operation.REMOVE:
                common.print_line('removing ' + op.src.remote+op.src.path)
                if op.src.is_dir:
                    try:
                        self.rmdir(op.src.path, op.src.remote)
                    except Exception as e:
                        logging.debug(str(e))
                else:
                    self.delete_file(op.src.path, op.src.remote)

    def restore_old(self, remote_path, local_dir):
        logging.debug('restoring directory ' + local_dir + ' from ' + remote_path)
        if not common.is_dir(local_dir):
            #logging.error('directory ' + local_dir + ' not found')
            common.print_line('destination directory ' + local_dir + ' not found!')
            return
            #raise Exception('directory ' + local_dir + ' not found')
        remote_clfiles = self.ls(remote_path)
        for remote_clfile in remote_clfiles:
            remote = remote_clfiles[remote_clfile].remote
            path = remote_clfiles[remote_clfile].path
            common.print_line('restoring file ' + remote+os.path.dirname(path) + ' -> ' + local_dir)
            logging.debug('restoring file ' + os.path.dirname(path) + ' from remote '
                          + remote)
            self.copy_new(remote+os.path.dirname(path), local_dir)


    def restore(self, remote_path, local_dir):
        logging.debug('restoring directory ' + local_dir + ' from ' + remote_path)
        if not common.is_dir(local_dir):
            #logging.error('directory ' + local_dir + ' not found')
            common.print_line('destination directory ' + local_dir + ' not found!')
            return
            #raise Exception('directory ' + local_dir + ' not found')
        for remote in self.get_remotes():
            common.print_line('restoring file ' + remote+remote_path + ' -> ' + local_dir)
            logging.debug('restoring file ' + remote+remote_path + ' -> ' + local_dir)
            self.copy_new(remote+remote_path, local_dir, True)


    def rmdir(self, directory, remote):
        logging.debug('removing directory ' + remote+directory)
        self._rclone.rmdir(remote, directory)

    def get_version(self):
        logging.debug('getting version')

    def touch(self, file):
        logging.debug('touching file ' + file)

    def delete_file(self, file, remote):
        logging.debug('deleting file ' + remote+file)
        self._rclone.delete_file(remote, file)

    def delete(self, path, remote):
        logging.debug('deleting path ' + remote+path)
        self._rclone.delete(remote, path)

    def copy(self, src, dst, remote):
        logging.debug('copy ' + src + ' to ' + remote + dst)
        self._rclone.copy(src, remote+dst)

    def copy_new(self, src, dst, no_error=False):
        logging.debug('copy ' + src + ' to ' + dst)
        self._rclone.copy(src, dst, [], no_error)

    def move(self, src, dst):
        logging.debug('move ' + src + ' to ' + dst)

    def sync(self, path):
        logging.debug('synchronize path ' + path)

