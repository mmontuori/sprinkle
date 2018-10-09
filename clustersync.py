#!/usr/bin/env python
"""
clustersync main module

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

from clsync import clsync
from mmontuori import config
from clsync import common
import logging
import getopt
import sys


def usage():
    print("usage: clustersync.py [-h] {-c|--conf <config file>} {command=None} {arg...arg}")
    print("       -h = help")
    print("       -c = configuration file")
    print("commands:")
    print("       ls = list files")
    print("   backup = backup files to clustered drives")


def usage_ls():
    print("usage: clustersync.py {-c|--conf <config file>} ls {pattern}")
    print("*** TO BE FINISHED ***")


def usage_backup():
    print("usage: clustersync.py {-c|--conf <config file>} backup {local dir}")
    print("*** TO BE FINISHED ***")


def read_args(argv):
    global __configfile
    global __dirtosync
    global __args

    try:
        opts, args = getopt.getopt(argv, "hc:", ["help", "conf="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ("-c", "--configfile"):
            __configfile = arg

    if len(args) < 1:
        usage()
        sys.exit()

    __args = args

    if __configfile == None or __configfile == '':
        usage()
        sys.exit(2)


def read_config(config_file):
    global __config
    conf = config.Config(config_file)
    __config = conf.get_config()


def init_logging(debug):
    if debug.lower() == "true":
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def ls():
    cl_sync = clsync.ClSync(__config)
    common.print_line('file list:')
    if len(__args) == 1:
        logging.error('invalid ls command')
        usage_ls()
        sys.exit(-1)
    files = cl_sync.lsjson(__args[1])
    logging.debug('files: ' + str(files))
    for tmp_file in files:
        if tmp_file.is_dir is True:
            first_chars = '-d-'
        else:
            first_chars = '---'
        common.print_line(first_chars + " " +
                          tmp_file.path.ljust(20) + " " +
                          str(tmp_file.size).rjust(9) + " " +
                          tmp_file.mod_time + " " +
                          tmp_file.remote
                          )


def backup():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid backup command')
        usage_backup()
        sys.exit(-1)
    local_dir = __args[1]
    common.print_line('backing up ' + local_dir + '...')
    cl_sync.backup(local_dir)


def main(argv):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    read_args(argv)
    read_config(__configfile)
    init_logging(__config['debug'])
    logging.debug('config: ' + str(__config))

    common.print_line('ClusterSync Utility')

    if __args[0] == 'ls':
        ls()
    elif __args[0] == 'backup':
        backup()
    else:
        logging.error('invalid command')
        usage()
        sys.exit(-1)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
