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
import logging
import getopt
import sys


def usage():
    print("usage: clustersync.py [-h] {-c|--conf <config file>} {command=None} {arg...arg}")
    print("       -h = help")
    print("       -c = configuration file")
    print("commands:")
    print("       ls = list files")


def usage_ls():
    print("usage: clustersync.py {-c|--conf <config file>} ls {pattern}")
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
        logging.info('debug mode initialized')
    else:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('info mode initialized')


def main(argv):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    read_args(argv)
    read_config(__configfile)
    init_logging(__config['debug'])
    logging.debug('config: ' + str(__config))

    cl_sync = clsync.ClSync(__config)

    if __args[0] == 'ls':
        logging.debug('command ls')
        if len(__args) == 1:
            logging.error('invalid ls command')
            usage_ls()
            sys.exit(-1)
        cl_sync.lsjson(__args[1])
    else:
        logging.error('invalid command')
        usage()
        sys.exit(-1)

    cl_sync.sync("/dirtosync")


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
