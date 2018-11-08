#!/usr/bin/env python3
"""
sprinkle_daemon : Daemon implementation for Sprinkle
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2018 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "0"
__docformat__ = "reStructuredText"

import time
import os
from libsprinkle import common
from libsprinkle import clsync
try:
    from daemons.prefab import run
except:
    print('Daemons library not found. run: "pip3 install daemons"')
    quit()
import logging

class SprinkleDaemon(run.RunDaemon):

    def __init__(self, config, local_dir):
        logging.info('initializing daemon mode on ' + os.name + '...')
        if os.name == 'nt':
            raise Exception('daemon cannot run on Windows')
        if config is None or local_dir is None:
            raise Exception('invalid parameters passed to daemon')
        self.__config = config
        self.__local_dir = local_dir

    def run(self):
        logging.info('starting daemom to backup path: ' + self.__local_dir)
        while True:
            global __cl_sync
            if __cl_sync is None:
                __cl_sync = clsync.ClSync(self.__config)
            local_dir = common.remove_ending_slash(self.__local_dir)
            common.print_line('backing up ' + local_dir + '...')
            __cl_sync.backup(local_dir, self.__config['delete_files'], self.__config['dry_run'])
            logging.debug('sleeping for ' + str(self.__config['daemon_interval']))
            time.sleep(self.__config['daemon_interval'])
