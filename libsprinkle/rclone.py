#!/usr/bin/env python3
"""
rclone wrapper module
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "2"

import logging
import json
from libsprinkle import common
from libsprinkle import exceptions

class RClone:

    def __init__(self, config_file=None, rclone_exe="rclone"):
        logging.debug('constructing RClone')
        if config_file is not None and not common.is_file(config_file):
            logging.error("configuration file " + str(config_file) + " not found. Cannot continue!")
            raise Exception("Configuration file " + str(config_file) + " not found")
        if rclone_exe is not "rclone" and not common.is_file(rclone_exe):
            logging.error("rclone executable " + str(rclone_exe) + " not found. Cannot continue!")
            common.print_line('RCLONE.EXE not in PATH. Put it in PATH or modify libsprinkle.conf to point to it.')
            raise Exception("rclone executable " + str(rclone_exe) + " not found")
        self._config_file = config_file
        self._rclone_exe = rclone_exe

    def get_remotes(self, extra_args=[]):
        logging.debug('listing remotes')
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("listremotes")
        for extra_arg in extra_args:
            command_with_args.append(extra_arg)
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['code'] == -20:
            logging.error("rclone executable not found. Please make sure it's in the PATH or in the config file")
            common.print_line("rclone executable not found. Please make sure it's in the PATH or in the config file")
            raise Exception("rclone executable not found. Please make sure it's in the PATH or in the config file")
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        remotes = result['out'].splitlines()
        return remotes

    def lsjson(self, remote, directory, extra_args=[], no_error=False):
        logging.debug('running lsjson for ' + remote + directory)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("lsjson")
        for extra_arg in extra_args:
            command_with_args.append(extra_arg)
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote+directory)
        result = common.execute(command_with_args, no_error)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            if no_error is False:
                #logging.error('error getting remotes objects')
                if result['error'].find("directory not found") != -1:
                    raise exceptions.FileNotFoundException(result['error'])
                else:
                    raise Exception('error getting remote object. ' + result['error'])
        lsjson = result['out']
        logging.debug('returning ' + str(lsjson))
        return lsjson

    def get_about(self, remote):
        logging.debug('running about for ' + remote)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("about")
        command_with_args.append("--json")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        aboutjson = result['out'].splitlines()
        logging.debug('returning ' + str(aboutjson))
        return aboutjson

    def mkdir(self, remote, directory):
        logging.debug('running mkdir for ' + remote + ":" + directory)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("mkdir")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote + directory)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def rmdir(self, remote, directory):
        logging.debug('running rmdir for ' + remote + ":" + directory)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("rmdir")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote + directory)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def get_version(self):
        logging.debug('running version')
        command_with_args = [self._rclone_exe, "version"]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def touch(self, remote, file):
        logging.debug('running touch for ' + remote + ":" + file)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("touch")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote + file)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def delete_file(self, remote, file):
        logging.debug('running deleteFile for ' + remote + ":" + file)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("deletefile")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote + file)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def delete(self, remote, file):
        logging.debug('running delete for ' + remote + ":" + file)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("delete")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote + file)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def copy(self, src, dst, extra_args=[], no_error=False):
        logging.debug('running copy from ' + src + " to " + dst)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("copy")
        for extra_arg in extra_args:
            command_with_args.append(extra_arg)
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(src)
        command_with_args.append(dst)
        logging.debug('command args: ' + str(command_with_args))
        result = common.execute(command_with_args, no_error)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            if no_error is False:
                logging.error('error getting remotes objects')
                raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def move(self, src, dst, extra_args=[]):
        logging.debug('running move from ' + src + " to " + dst)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("move")
        for extra_arg in extra_args:
            command_with_args.append(extra_arg)
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(src)
        command_with_args.append(dst)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def get_free(self, remote):
        logging.debug('running about for ' + remote)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("about")
        command_with_args.append("--json")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        aboutjson = result['out']
        json_obj = json.loads(aboutjson)
        logging.debug('free ' + str(json_obj['free']))
        return json_obj['free']

    def get_size(self, remote):
        logging.debug('running about for ' + remote)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("about")
        command_with_args.append("--json")
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file)
        command_with_args.append(remote)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        aboutjson = result['out']
        json_obj = json.loads(aboutjson)
        logging.debug('total ' + str(json_obj['total']))
        return json_obj['total']

    def sync(self, src, dst, extra_args=[]):
        logging.debug('running sync from ' + src + " to " + dst)
        command_with_args = []
        command_with_args.append(self._rclone_exe)
        command_with_args.append("sync")
        for extra_arg in extra_args:
            command_with_args.append(extra_arg)
        if self._config_file is not None:
            command_with_args.append("--config")
            command_with_args.append(self._config_file, src, dst)
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out


