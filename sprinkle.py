#!/usr/bin/env python3
"""
libsprinkle main module
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "2"

from libsprinkle import clsync
from libsprinkle import rclone
from libsprinkle import config
from libsprinkle import common
import logging
import getopt
import sys


def usage():
    print("usage: sprinkle.py [options} {command=None} {arg...arg}")
    print("  options:")
    print("    -h|--help     = help")
    print("    -c|--conf     = configuration file")
    print("    -v|--version  = print version")
    print("    -d|--debug    = debug output")
    print("    --dist-type   = distribution type (defaults:mas)")
    print("    --comp-method = compare method (defaults:size)")
    print("    --rclone-exe = rclone executable (defaults:rclone)")
    print("    --rclone-conf = rclone configuration (defaults:None)")
    print("   --display_unit = display unit [G|M|K|B]")
    print("  commands:")
    print("         ls = list files")
    print("     backup = backup files to clustered drives")
    print("    restore = restore files from clustered drives")
    print("      stats = display volume statistics")


def usage_ls():
    print("usage: sprinkle.py {-c|--conf <config file>} ls {pattern}")
    print("*** TO BE FINISHED ***")


def usage_backup():
    print("usage: sprinkle.py {-c|--conf <config file>} backup {local dir}")
    print("*** TO BE FINISHED ***")


def usage_restore():
    print("usage: sprinkle.py {-c|--conf <config file>} restore {remote dir} {local dir}")
    print("*** TO BE FINISHED ***")


def usage_stats():
    print("usage: sprinkle.py {-c|--conf <config file>} stats [volume]")
    print("*** TO BE FINISHED ***")


def print_version():
    print("sprinkle version: " + __version__ + '.' + __revision__)
    print("sprinkle module version: " + clsync.__version__ + '.' + clsync.__revision__)
    print("rclone module version: " + rclone.__version__ + '.' + rclone.__revision__)


def read_args(argv):
    global __configfile
    global __dirtosync
    global __args
    global __cmd_debug
    global __dist_type
    global __comp_method
    global __rclone_exe
    global __rclone_conf
    global __display_unit

    __configfile = None
    __cmd_debug = False
    __dist_type = None
    __comp_method = None
    __rclone_exe = None
    __rclone_conf = None
    __display_unit = 'G'

    try:
        opts, args = getopt.getopt(argv, "dvhc:s:",
                                   ["help",
                                    "conf=",
                                    "debug",
                                    "version",
                                    "dist-type=",
                                    "comp-method=",
                                    "rclone-exe=",
                                    "rclone-conf=",
                                    "stats=",
                                    "display-unit="])
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
        elif opt in ("-d", "--debug"):
            __cmd_debug = True
        elif opt in ("--dist-type"):
            __dist_type = arg
        elif opt in ("--comp-method"):
            __comp_method = arg
        elif opt in ("--rclone-exe"):
            __rclone_exe = arg
        elif opt in ("--rclone-conf"):
            __rclone_conf = arg
        elif opt in ("--display-unit"):
            if arg != 'G' and arg != 'M' and arg != 'K' and arg != 'B':
                logging.error('invalid UNIT ' + arg + ', only [G|M|K|B] accepted')
            __display_unit = arg


    if len(args) < 1:
        usage()
        sys.exit()

    __args = args


def read_config(config_file):
    global __config
    if config_file is not None:
        conf = config.Config(config_file)
        __config = conf.get_config()
    else:
        __config = {}


def init_logging(debug):
    if debug.lower() == "true":
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def ls():
    cl_sync = clsync.ClSync(__config)
    common.print_line('retrieving file list...')
    if len(__args) == 1:
        logging.error('invalid ls command')
        usage_ls()
        sys.exit(-1)
    files = cl_sync.ls(common.remove_ending_slash(__args[1]))
    largest_length = 25
    for tmp_file in files:
        filename_length = len(files[tmp_file].path)
        if not files[tmp_file].is_dir and filename_length > largest_length:
            largest_length = filename_length
    common.print_line('---' + " " +
                      'NAME'.ljust(largest_length) + " " +
                      'SIZE'.rjust(9) + " " +
                      'MOD TIME'.ljust(25) + " " +
                      'REMOTE'
                      )
    common.print_line('---' + " " +
                      ''.join('-' for i in range(largest_length)) + " " +
                      ''.join('-' for i in range(9)) + " " +
                      ''.join('-' for i in range(25)) + " " +
                      ''.join('-' for i in range(15))
                      )

    for tmp_file in files:
        if files[tmp_file].is_dir is True:
            first_chars = '-d-'
        else:
            first_chars = '---'
        file_name = files[tmp_file].path
        if file_name.startswith('//'):
            file_name = file_name[1:len(file_name)]
        common.print_line(first_chars + " " +
                          file_name.ljust(largest_length) + " " +
                          str(files[tmp_file].size).rjust(9) + " " +
                          files[tmp_file].mod_time.ljust(25) + " " +
                          files[tmp_file].remote
                          )


def backup():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid backup command')
        usage_backup()
        sys.exit(-1)
    local_dir = common.remove_ending_slash(__args[1])
    common.print_line('backing up ' + local_dir + '...')
    cl_sync.backup(local_dir)


def restore():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 2:
        logging.error('invalid remote command')
        usage_restore()
        sys.exit(-1)
    remote_path = __args[2]
    local_dir = common.remove_ending_slash(__args[1])
    common.print_line('restoring ' + local_dir + ' from ' + remote_path)
    cl_sync.restore(local_dir, remote_path)


def stats():
    logging.debug('display stats about the volumes')
    common.print_line('calculating total and free space...')
    cl_sync = clsync.ClSync(__config)
    common.print_line('REMOTE'.ljust(15) + " " +
                      'SIZE'.rjust(20) + " " +
                      'FREE'.rjust(20) + " " +
                      '%FREE'.rjust(10)
                      )
    common.print_line(''.join('=' for i in range(15)) + " " +
                      ''.join('=' for i in range(20)) + " " +
                      ''.join('=' for i in range(20)) + " " +
                      ''.join('=' for i in range(10))
                      )
    sizes = cl_sync.get_sizes()
    frees = cl_sync.get_frees()
    for remote in sizes:
        percent_use = frees[remote] * 100 / sizes[remote]
        size_d = common.convert_unit(sizes[remote], __display_unit)
        free_d = common.convert_unit(frees[remote], __display_unit)
        common.print_line(remote.ljust(15) + " " +
                          "{:,}".format(size_d).rjust(19) + __display_unit + " " +
                          "{:,}".format(free_d).rjust(19) + __display_unit + " " +
                          "{:,}".format(int(percent_use)).rjust(10)
                          )

    size = cl_sync.get_size()
    free = cl_sync.get_free()
    logging.debug('size: ' + "{:,}".format(size))
    logging.debug('free: ' + "{:,}".format(free))
    percent_use = free * 100 / size
    common.print_line(''.join('-' for i in range(15)) + " " +
                      ''.join('-' for i in range(20)) + " " +
                      ''.join('-' for i in range(20)) + " " +
                      ''.join('-' for i in range(10))
                      )
    size_d = common.convert_unit(size, __display_unit)
    free_d = common.convert_unit(free, __display_unit)
    common.print_line("total:".ljust(15) + " " +
                      "{:,}".format(size_d).rjust(19) + __display_unit + " " +
                      "{:,}".format(free_d).rjust(19) + __display_unit + " " +
                      "{:,}".format(int(percent_use)).rjust(10)
                      )


def main(argv):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    read_args(argv)
    read_config(__configfile)
    if __cmd_debug is True:
        init_logging('true')
    elif 'debug' in __config:
        init_logging(__config['debug'])
    if __dist_type is not None:
        __config['distribution_type'] = __dist_type
    if __comp_method is not None:
        __config['compare_method'] = __comp_method
    if __rclone_exe is not None:
        __config['rclone_exe'] = __rclone_exe
    if __rclone_conf is not None:
        __config['rclone_config'] = __rclone_conf
    logging.debug('config: ' + str(__config))

    common.print_line('Sprinkle Utility')

    if __args[0] == 'ls':
        ls()
    elif __args[0] == 'backup':
        backup()
    elif __args[0] == 'restore':
        restore()
    elif __args[0] == 'stats':
        stats()
    else:
        logging.error('invalid command')
        usage()
        sys.exit(-1)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
