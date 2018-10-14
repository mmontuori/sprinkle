#!/usr/bin/env python3
"""
sprinkle main module
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
__revision__ = "2"

from sprinkle import clsync
from sprinkle import rclone
from sprinkle import config
from sprinkle import common
import logging
import getopt
import sys


def usage():
    print("usage: sprinkle.py [-v] [-h] {-c|--conf <config file>} {command=None} {arg...arg}")
    print("       -h = help")
    print("       -c = configuration file")
    print("       -v = print version")
    print("commands:")
    print("       ls = list files")
    print("   backup = backup files to clustered drives")
    print("  restore = restore files from clustered drives")


def usage_ls():
    print("usage: sprinkle.py {-c|--conf <config file>} ls {pattern}")
    print("*** TO BE FINISHED ***")


def usage_backup():
    print("usage: sprinkle.py {-c|--conf <config file>} backup {local dir}")
    print("*** TO BE FINISHED ***")


def usage_restore():
    print("usage: sprinkle.py {-c|--conf <config file>} restore {remote dir} {local dir}")
    print("*** TO BE FINISHED ***")


def print_version():
    print("sprinkle version: " + __version__ + '.' + __revision__)
    print("sprinkle module version: " + clsync.__version__ + '.' + clsync.__revision__)
    print("rclone module version: " + rclone.__version__ + '.' + rclone.__revision__)


def read_args(argv):
    global __configfile
    global __dirtosync
    global __args

    try:
        opts, args = getopt.getopt(argv, "vhc:", ["help", "conf="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-v', '--version'):
            print_version()
            sys.exit(0)
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
    files = cl_sync.ls(__args[1])
    largest_length = 25
    for tmp_file in files:
        filename_length = len(files[tmp_file].path)
        if not files[tmp_file].is_dir and filename_length > largest_length:
            largest_length = filename_length
    for tmp_file in files:
        if files[tmp_file].is_dir is True:
            first_chars = '-d-'
        else:
            first_chars = '---'
        common.print_line(first_chars + " " +
                          files[tmp_file].path.ljust(largest_length) + " " +
                          str(files[tmp_file].size).rjust(9) + " " +
                          files[tmp_file].mod_time + " " +
                          files[tmp_file].remote
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


def restore():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 2:
        logging.error('invalid remote command')
        usage_restore()
        sys.exit(-1)
    remote_path = __args[2]
    local_dir = __args[1]
    common.print_line('restoring ' + local_dir + ' from ' + remote_path)
    cl_sync.restore(local_dir, remote_path)


def main(argv):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    read_args(argv)
    read_config(__configfile)
    init_logging(__config['debug'])
    logging.debug('config: ' + str(__config))

    common.print_line('Sprinkle Utility')

    if __args[0] == 'ls':
        ls()
    elif __args[0] == 'backup':
        backup()
    elif __args[0] == 'restore':
        restore()
    else:
        logging.error('invalid command')
        usage()
        sys.exit(-1)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
