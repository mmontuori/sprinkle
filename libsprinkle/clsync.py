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
from progress.bar import Bar
import json
import os

class ClSync:

    duplicate_suffix = ".sprinkle_duplicate_file"

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
        if 'rclone_retries' not in config:
            self._rclone_retries = '1'
        else:
            self._rclone_retries = config['rclone_retries']
        self._remotes = None
        self._remote_calls = 0
        self._sizes = None
        self._frees = None
        self._show_progress = config['show_progress']

        if 'rclone_exe' not in self._config:
            self._rclone = rclone.RClone(rclone_config)
        else:
            self._rclone = rclone.RClone(rclone_config, self._config['rclone_exe'], self._rclone_retries)

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

    def ls(self, file, with_dups=False):
        logging.debug('lsjson of file: ' + file)
        if not file.startswith('/'):
            file = '/' + file
        files = {}
        md5s = None
        if self._compare_method == 'md5':
            md5s = self.lsmd5(file)
        for remote in self.get_remotes():
            common.print_line('retrieving file list from: ' + remote + file + '...')
            logging.debug('getting lsjson from ' + remote + file)
            try:
                json_out = self._rclone.lsjson(remote, file, ['--recursive', '--fast-list'], True)
            except exceptions.FileNotFoundException as e:
                json_out = '[]'
            logging.debug('loading json')
            tmp_json = json.loads(json_out)
            logging.debug('json size: ' + str(len(tmp_json)))
            logging.debug('json loaded')
            for tmp_json_file in tmp_json:
                tmp_file = clfile.ClFile()
                tmp_file.remote = remote
                tmp_file.path = file + '/' + tmp_json_file['Path']
                tmp_file.name = tmp_json_file['Name']
                tmp_file.size = tmp_json_file['Size']
                tmp_file.mime_type = tmp_json_file['MimeType']
                tmp_file.mod_time = tmp_json_file['ModTime']
                tmp_file.is_dir = tmp_json_file['IsDir']
                tmp_file.id = tmp_json_file['ID']
                key = file + '/' + tmp_json_file['Path']
                if self._compare_method == 'md5' and not tmp_file.is_dir:
                    tmp_file.md5 = md5s[key]
                if with_dups and tmp_file.is_dir is False and key in files:
                    key = key + ClSync.duplicate_suffix
                files[key] = tmp_file
            logging.debug('end of clsync.ls()')
        return files

    def lsmd5(self, file):
        logging.debug('lsjson of file: ' + file)
        if not file.startswith('/'):
            file = '/' + file
        files = {}
        for remote in self.get_remotes():
            common.print_line('retrieving file list from: ' + remote + file + '...')
            logging.debug('getting lsjson from ' + remote + file)
            try:
                out = self._rclone.md5sum(remote, file, ['--fast-list'], True)
            except exceptions.FileNotFoundException as e:
                out = ''
            #logging.debug('out: ' + str(out.split('\n')))
            md5s = out.split('\n')
            for line in md5s:
                if line == '':
                    continue
                md5 = line.split('  ')[0]
                filename = line.split('  ')[1]
                files[file + '/' + filename] = md5
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
        common.print_line('indexing local directory: ' + local_dir + '...')
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
                if self._compare_method == 'md5':
                    tmp_clfile.md5 = common.get_md5(full_path)
                clfiles[common.normalize_path(tmp_clfile.path+'/'+tmp_clfile.name)] = tmp_clfile
        logging.debug('retrieved ' + str(len(clfiles)) + ' files')
        return clfiles

    def compare_clfiles(self, local_dir, local_clfiles, remote_clfiles, delete_file=False):
        common.print_line('calculating differences...')
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
                elif self._compare_method == 'md5':
                    local_md5 = local_clfile.md5
                    remote_md5 = remote_clfile.md5
                    current_remote = remote_clfiles[rel_name].remote
                    logging.debug('local_file.md5:' + str(local_md5) +
                                  ', remote_clfile.md5:' + str(remote_md5))
                    if local_md5 != remote_md5:
                        logging.debug('file has changed')
                        local_clfile.remote_path = rel_path
                        local_clfile.remote = current_remote
                        op = operation.Operation(operation.Operation.UPDATE,
                                                 local_clfile, None)
                        operations.append(op)
                else:
                    logging.error('compare_method: ' + self._compare_method + ' not valid!')
                    raise Exception('compare_method: ' + self._compare_method + ' not valid!')

        if delete_file is True:
            for remote_path in remote_clfiles:
                remote_clfile = remote_clfiles[remote_path]
                logging.debug('checking file ' + remote_dir+remote_path + ' for deletion')
                rel_name = common.remove_localdir(local_dir, remote_clfile.path + '/' + remote_clfile.name)
                rel_path = common.remove_localdir(local_dir, remote_clfile.path)
                logging.debug('relative name: ' + rel_name)
                if remote_dir+remote_path not in local_clfiles:
                    logging.debug('file ' + remote_path + ' has been deleted')
                    remote_clfile.remote_path = rel_path
                    op = operation.Operation(operation.Operation.REMOVE,
                                             remote_clfile, None)
                    operations.append(op)
        common.print_line('found ' + str(len(operations)) + ' differences')
        return operations

    def backup(self, local_dir, delete_files=False, dry_run=False):
        logging.debug('backing up directory ' + local_dir)
        if not common.is_dir(local_dir):
            logging.error("local directory " + local_dir + " not found. Cannot continue!")
            raise Exception("Local directory " + local_dir + " not found")
        local_clfiles = self.index_local_dir(local_dir)
        remote_clfiles = self.ls(os.path.basename(local_dir))
        ops = self.compare_clfiles(local_dir, local_clfiles, remote_clfiles, delete_files)
        if len(ops) > 0 and self._show_progress:
            bar = Bar('Progress', max=len(ops), suffix='%(index)d/%(max)d %(percent)d%% [%(elapsed_td)s/%(eta_td)s]')
        else:
            common.print_line('no action necessary')
        if dry_run is True:
            common.print_line('performing a dry run. no changes are committed')
        for op in ops:
            logging.debug('operation: ' + op.operation + ", path: " + op.src.path)
            if self._show_progress:
                bar_title = op.src.name.ljust(25, '.')
                if len(bar_title) > 25:
                    bar_title = bar_title[0:25]
                bar.message = 'file:' + bar_title
            if op.src.is_dir and op.operation != operation.Operation.REMOVE:
                logging.debug('skipping directory ' + op.src.path)
                continue
            if op.operation == operation.Operation.ADD:
                best_remote = self.get_best_remote(int(op.src.size))
                logging.debug('best remote: ' + best_remote)
                if not self._show_progress:
                    common.print_line('backing up file ' + op.src.path+'/'+op.src.name +
                                  ' -> ' + best_remote+':'+op.src.remote_path)
                if dry_run is False:
                    self.copy(op.src.path+'/'+op.src.name, op.src.remote_path, best_remote)
            if op.operation == operation.Operation.UPDATE:
                best_remote = self.get_best_remote(int(op.src.size))
                logging.debug('best remote: ' + best_remote)
                if not self._show_progress:
                    common.print_line('backing up file ' + op.src.path + '/' + op.src.name +
                                  ' -> ' + op.src.remote + ':' + op.src.remote_path)
                if dry_run is False:
                    self.copy(op.src.path + '/' + op.src.name, op.src.remote_path, op.src.remote)
            if op.operation == operation.Operation.REMOVE and delete_files:
                if not self._show_progress:
                    common.print_line('removing ' + op.src.remote+op.src.path)
                if op.src.is_dir:
                    if dry_run is False:
                        try:
                            self.rmdir(op.src.path, op.src.remote)
                        except Exception as e:
                            logging.debug(str(e))
                else:
                    if dry_run is False:
                        self.delete_file(op.src.path, op.src.remote)
            if self._show_progress:
                bar.next()
        if  len(ops) > 0 and self._show_progress:
            bar.finish()

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


    def restore(self, remote_path, local_dir, dry_run=False):
        logging.debug('restoring directory ' + local_dir + ' from ' + remote_path)
        if not common.is_dir(local_dir):
            #logging.error('directory ' + local_dir + ' not found')
            common.print_line('destination directory ' + local_dir + ' not found!')
            return
            #raise Exception('directory ' + local_dir + ' not found')
        for remote in self.get_remotes():
            common.print_line('restoring file ' + remote+remote_path + ' -> ' + local_dir)
            logging.debug('restoring file ' + remote+remote_path + ' -> ' + local_dir)
            if dry_run is False:
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

    def remove_duplicates(self, path):
        files = self.ls(path, True)
        common.print_line('analyzing for duplications...')
        keys = common.sort_dict_keys(files)
        for key in keys:
            if key.endswith(ClSync.duplicate_suffix):
                logging.debug('found duplicate file: ' + key)
                date1 = common.get_datetime_from_iso8601(files[key].mod_time)
                logging.debug(key + ' timestamp: ' + str(date1.timestamp()))
                key2 = key.replace(ClSync.duplicate_suffix, '')
                date2 = common.get_datetime_from_iso8601(files[key2].mod_time)
                logging.debug(key2 + ' timestamp: ' + str(date2.timestamp()))
                if date1.timestamp() > date2.timestamp():
                    logging.debug(key + ' is newer than ' + key2)
                    file_to_remove = files[key2].remote + key2
                    common.print_line('found duplicate file. Removing: ' + file_to_remove + '...')
                    self.delete_file(key2, files[key2].remote)
                elif date1.timestamp() == date1.timestamp():
                    logging.debug(key + ' is equal to ' + key2)
                    file_to_remove = files[key2].remote + key2
                    common.print_line('found duplicate file. Removing: ' + file_to_remove + '...')
                    self.delete_file(key2, files[key2].remote)
                else:
                    logging.debug(key + ' is older than ' + key2)
                    file_to_remove = files[key].remote + key
                    common.print_line('found duplicate file. Removing: ' + file_to_remove + '...')
                    self.delete_file(key, files[key].remote)
                logging.debug('file to remove: ' + file_to_remove)
