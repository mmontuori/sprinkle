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
import subprocess
import os.path

class RClone:

    def __init__(self, config_file, rclone_exe="rclone"):
        logging.debug('constructing RClone')
        if config_file == None:
            logging.error("configuration file " + str(config_file) + " is None. Cannot continue!")
            raise Exception("None value for configuration file")
        if not os.path.isfile(config_file):
            logging.error("configuration file " + str(config_file) + " not found. Cannot continue!")
            raise Exception("Configuration file not found")
        if rclone_exe is not "rclone" and not os.path.isfile(rclone_exe):
            logging.error("rclone executable " + str(rclone_exe) + " not found. Cannot continue!")
            raise Exception("rclone executable not found")
        self._config_file = config_file
        self._rclone_exe = rclone_exe

    def _execute(self, command_with_args):
        logging.debug("Invoking : %s", " ".join(command_with_args))
        try:
            with subprocess.Popen(
                    command_with_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE) as proc:
                (out, err) = proc.communicate()

                # out = proc.stdout.read()
                # err = proc.stderr.read()

                logging.debug(out)
                if err:
                    logging.warning(err.decode("utf-8").replace("\\n", "\n"))

                return {
                    "code": proc.returncode,
                    "out": out.decode('ASCII'),
                    "error": err.decode('ASCII')
                }
        except FileNotFoundError as not_found_e:
            logging.error("Executable not found. %s", not_found_e)
            return {
                "code": -20,
                "error": not_found_e
            }
        except Exception as generic_e:
            logging.exception("Error running command. Reason: %s", generic_e)
            return {
                "code": -30,
                "error": generic_e
            }

    def get_remotes(self):
        logging.debug('listing remotes')
        command_with_args = [self._rclone_exe, "listremotes", "--config", self._config_file]
        result = self._execute(command_with_args)
        logging.debug('result: ' + result['error'])
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        remotes = result['out'].splitlines()
        return remotes

    def get_lsjson(self, remote, directory):
        logging.debug('running lsjson for ' + remote + ":" + directory)
        command_with_args = [self._rclone_exe, "lsjson", "--config", self._config_file, remote+directory]
        result = self._execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        lsjson = result['out'].splitlines()
        logging.debug('returning ' + str(lsjson))
        return lsjson

    def get_about(self, remote):
        logging.debug('running about for ' + remote)
        command_with_args = [self._rclone_exe, "about", "--json", "--config", self._config_file, remote]
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
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
        result = self._execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return None

    def move(self, src, dst):
        logging.debug('running move from ' + src + " to " + dst)
        command_with_args = [self._rclone_exe, "move", "--config", self._config_file, src, dst]
        result = self._execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        out = result['out'].splitlines()
        logging.debug('returning ' + str(out))
        return None


