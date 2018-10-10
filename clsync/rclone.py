#!/usr/bin/env python
"""
rclone wrapper module

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

import logging
import json
from clsync import common
from clsync import exceptions

class RClone:

    def __init__(self, config_file, rclone_exe="rclone"):
        logging.debug('constructing RClone')
        if config_file == None:
            logging.error("configuration file " + str(config_file) + " is None. Cannot continue!")
            raise Exception("None value for configuration file")
        if not common.is_file(config_file):
            logging.error("configuration file " + str(config_file) + " not found. Cannot continue!")
            raise Exception("Configuration file " + str(config_file) + " not found")
        if rclone_exe is not "rclone" and not common.is_file(rclone_exe):
            logging.error("rclone executable " + str(rclone_exe) + " not found. Cannot continue!")
            raise Exception("rclone executable " + str(rclone_exe) + " not found")
        self._config_file = config_file
        self._rclone_exe = rclone_exe

    def get_remotes(self):
        logging.debug('listing remotes')
        command_with_args = [self._rclone_exe, "listremotes", "--config", self._config_file]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        remotes = result['out'].splitlines()
        return remotes

    def lsjson(self, remote, directory):
        # TBD recursive lsjson
        logging.debug('running lsjson for ' + remote + directory)
        command_with_args = [self._rclone_exe, "lsjson", "--config", self._config_file, remote+directory]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            if result['error'].find("directory not found") != -1:
                raise exceptions.FileNotFoundException(result['error'])
            else:
                raise Exception('error getting remote object. ' + result['error'])
        lsjson = result['out']
        logging.debug('returning ' + str(lsjson))
        return lsjson

    def get_about(self, remote):
        logging.debug('running about for ' + remote)
        command_with_args = [self._rclone_exe, "about", "--json", "--config", self._config_file, remote]
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
        command_with_args = [self._rclone_exe, "mkdir", "--config", self._config_file, remote + directory]
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
        command_with_args = [self._rclone_exe, "rmdir", "--config", self._config_file, remote + directory]
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
        command_with_args = [self._rclone_exe, "touch", "--config", self._config_file, remote + file]
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
        command_with_args = [self._rclone_exe, "deletefile", "--config", self._config_file, remote + file]
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
        command_with_args = [self._rclone_exe, "delete", "--config", self._config_file, remote + file]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def copy(self, src, dst):
        logging.debug('running copy from ' + src + " to " + dst)
        command_with_args = [self._rclone_exe, "copy", "--config", self._config_file, src, dst]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out

    def move(self, src, dst):
        logging.debug('running move from ' + src + " to " + dst)
        command_with_args = [self._rclone_exe, "move", "--config", self._config_file, src, dst]
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
        command_with_args = [self._rclone_exe, "about", "--json", "--config", self._config_file, remote]
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
        command_with_args = [self._rclone_exe, "about", "--json", "--config", self._config_file, remote]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        aboutjson = result['out']
        json_obj = json.loads(aboutjson)
        logging.debug('total ' + str(json_obj['total']))
        return json_obj['total']

    def sync(self, src, dst):
        logging.debug('running sync from ' + src + " to " + dst)
        command_with_args = [self._rclone_exe, "sync", "--config", self._config_file, src, dst]
        result = common.execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return out


