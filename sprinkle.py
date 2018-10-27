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
from libsprinkle import smtp_email
import logging
import getopt
import sys
import traceback


def print_heading():
    print("***********************************************")
    print('* sprinkle the cloud clustered backup utility *')
    print("***********************************************")

def usage():
    print("usage: sprinkle.py [options} {command=None} {arg...arg}")
    print("  options:")
    print("    -h|--help     = help")
    print("    -c|--conf     = configuration file")
    print("    -v|--version  = print version")
    print("    -d|--debug    = debug output")
    print("    --dist-type   = distribution type (defaults:mas)")
    print("    --comp-method = compare method [size|md5] (defaults:size)")
    print("     --rclone-exe = rclone executable (defaults:rclone)")
    print("    --rclone-conf = rclone configuration (defaults:None)")
    print("   --display_unit = display unit [G|M|K|B]")
    print("        --retries = number of retries (default:1)")
    print("  --show-progress = show progress")
    print("   --delete-after = delete files on remote end (defaults:false)")
    print("        --dry-run = perform a dry run without actually backing up")
    print("  commands:")
    print("         ls = list files")
    print("      lsmd5 = list md5 of files")
    print("     backup = backup files to clustered drives")
    print("    restore = restore files from clustered drives")
    print("      stats = display volume statistics")
    print(" removedups = removes duplicate files")


def usage_ls():
    print("usage: sprinkle.py {-c|--conf <config file>} ls {pattern}")
    print("*** TO BE FINISHED ***")


def usage_lsmd5():
    print("usage: sprinkle.py {-c|--conf <config file>} lsmd5 {pattern}")
    print("*** TO BE FINISHED ***")


def usage_backup():
    print("usage: sprinkle.py {-c|--conf <config file>} backup {local dir}")
    print("*** TO BE FINISHED ***")


def usage_restore():
    print("usage: sprinkle.py {-c|--conf <config file>} restore {remote dir} {local dir}")
    print("*** TO BE FINISHED ***")


def usage_stats():
    print("usage: sprinkle.py {-c|--conf <config file>} stats")
    print("*** TO BE FINISHED ***")


def usage_removedups():
    print("usage: sprinkle.py {-c|--conf <config file>} removedups [pattern]")
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
    global __rclone_retries
    global __show_progress
    global __delete_files
    global __dry_run
    global __smtp_enable
    global __smtp_from
    global __smtp_to
    global __smtp_server
    global __smtp_port
    global __smtp_user
    global __smtp_password

    __configfile = None
    __cmd_debug = None
    __dist_type = None
    __comp_method = None
    __rclone_exe = None
    __rclone_conf = None
    __display_unit = None
    __rclone_retries = None
    __show_progress = None
    __delete_files = None
    __dry_run = None
    __smtp_enable = None
    __smtp_from = None
    __smtp_to = None
    __smtp_server = None
    __smtp_port = None
    __smtp_user = None
    __smtp_password = None

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
                                    "display-unit=",
                                    "rclone-retries=",
                                    "show-progress",
                                    "dry-run",
                                    "delete-files",
                                    "smtp-enable",
                                    "smtp-from=",
                                    "smtp-to=",
                                    "smtp-server=",
                                    "smtp-port=",
                                    "smtp-user=",
                                    "smtp-password="
                                    ])
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
        elif opt in ("-c", "--conf"):
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
        elif opt in ("--rclone-retries"):
            __rclone_retries = int(arg)
        elif opt in ("--show-progress"):
            __show_progress = True
        elif opt in ("--delete-files"):
            __delete_files = True
        elif opt in ("--dry-run"):
            __dry_run = True
        elif opt in ("--smtp-enable"):
            __smtp_enable = True
        elif opt in ("--smtp-from"):
            __smtp_from = arg
        elif opt in ("--smtp-to"):
            __smtp_to = arg
        elif opt in ("--smtp-server"):
            __smtp_server = arg
        elif opt in ("--smtp-port"):
            __smtp_port = arg
        elif opt in ("--smtp-user"):
            __smtp_user = arg
        elif opt in ("--smtp-password"):
            __smtp_password = arg

    if len(args) < 1:
        usage()
        sys.exit()

    __args = args


def configure(config_file):
    global __config

    _default_fields = [
        "debug",
        "dry_run",
        "show_progress",
        "delete_files",
        "smtp_enable",
        "distribution_type",
        "compare_method",
        "display_unit",
        'rclone_retries'
    ]

    _default_values = {
        "debug": False,
        "dry_run": False,
        "show_progress": False,
        "delete_files": True,
        "smtp_enable": False,
        "distribution_type": "mas",
        "compare_method": "size",
        "display_unit": "G",
        "rclone_retries": '1'
    }

    if config_file is not None:
        conf = config.Config(config_file)
        __config = conf.get_config()
    else:
        __config = {}

    for field in _default_fields:
        if field not in __config:
            __config[field] = _default_values[field]

    if __cmd_debug is True:
        init_logging(True)
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

    if __rclone_retries is not None:
        __config['rclone_retries'] = str(__rclone_retries)

    if __show_progress is not None:
        __config['show_progress'] = __show_progress

    if __delete_files is not None:
        __config['delete_files'] = __delete_files

    if __dry_run is not None:
        __config['dry_run'] = __dry_run

    if __smtp_enable is not None:
        __config['smtp_enable'] = __smtp_enable

    if __display_unit is not None:
        __config['display_unit'] = __display_unit

    if __smtp_from is not None:
        __config['smtp_from'] = __smtp_from

    if __smtp_to is not None:
        __config['smtp_to'] = __smtp_to

    if __smtp_server is not None:
        __config['smtp_server'] = __smtp_server

    if __smtp_port is not None:
        __config['smtp_port'] = __smtp_port

    if __smtp_user is not None:
        __config['smtp_user'] = __smtp_user

    if __smtp_password is not None:
        __config['smtp_password'] = __smtp_password


def verify_configuration():
    logging.debug('verifying configuration ' + str(__config))
    if __config['smtp_enable'] is True:
        if 'smtp_from' not in __config:
            raise Exception('smtp_from value is None')
        if 'smtp_to' not in __config:
            raise Exception('smtp_to value is None')
        if 'smtp_server' not in __config:
            raise Exception('smtp_server value is None')
        if 'smtp_port' not in __config:
            raise Exception('smtp_port value is None')


def init_logging(debug):
    if debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def ls():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid ls command')
        usage_ls()
        sys.exit(-1)
    files = cl_sync.ls(common.remove_ending_slash(__args[1]))
    largest_length = 25
    keys = common.sort_dict_keys(files)
    for tmp_file in keys:
        filename_length = len(files[tmp_file].path)
        if not files[tmp_file].is_dir and filename_length > largest_length:
            largest_length = filename_length
    common.print_line('---' + " " +
                      'NAME'.ljust(largest_length) + " " +
                      'SIZE'.rjust(9) + " " +
                      'MOD TIME'.ljust(19) + " " +
                      'REMOTE'
                      )
    common.print_line('---' + " " +
                      ''.join('-' for i in range(largest_length)) + " " +
                      ''.join('-' for i in range(9)) + " " +
                      ''.join('-' for i in range(19)) + " " +
                      ''.join('-' for i in range(15))
                      )

    for tmp_file in keys:
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
                          common.get_printable_datetime(files[tmp_file].mod_time).ljust(19) + " " +
                          files[tmp_file].remote
                          )

def lsmd5():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid ls command')
        usage_lsmd5()
        sys.exit(-1)
    files = cl_sync.lsmd5(common.remove_ending_slash(__args[1]))
    largest_length = 25
    keys = common.sort_dict_keys(files)
    for tmp_file in keys:
        filename_length = len(tmp_file)
        if filename_length > largest_length:
            largest_length = filename_length
    common.print_line('NAME'.ljust(largest_length) + " " +
                      'MD5'.ljust(32)
                      )
    common.print_line(''.join('-' for i in range(largest_length)) + " " +
                      ''.join('-' for i in range(32))
                      )

    for tmp_file in keys:
        file_name = tmp_file
        common.print_line(file_name.ljust(largest_length) + " " +
                          files[tmp_file]
                          )

def backup():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid backup command')
        usage_backup()
        sys.exit(-1)
    local_dir = common.remove_ending_slash(__args[1])
    common.print_line('backing up ' + local_dir + '...')
    cl_sync.backup(local_dir, __config['delete_files'], __config['dry_run'])


def restore():
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 2:
        logging.error('invalid remote command')
        usage_restore()
        sys.exit(-1)
    remote_path = __args[2]
    local_dir = common.remove_ending_slash(__args[1])
    common.print_line('restoring ' + local_dir + ' from ' + remote_path)
    cl_sync.restore(local_dir, remote_path, __config['dry_run'])


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
    display_unit = __config['display_unit']
    for remote in sizes:
        percent_use = frees[remote] * 100 / sizes[remote]
        size_d = common.convert_unit(sizes[remote], display_unit)
        free_d = common.convert_unit(frees[remote], display_unit)
        common.print_line(remote.ljust(15) + " " +
                          "{:,}".format(size_d).rjust(19) + display_unit + " " +
                          "{:,}".format(free_d).rjust(19) + display_unit + " " +
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
    size_d = common.convert_unit(size, display_unit)
    free_d = common.convert_unit(free, display_unit)
    common.print_line("total:".ljust(15) + " " +
                      "{:,}".format(size_d).rjust(19) + display_unit + " " +
                      "{:,}".format(free_d).rjust(19) + display_unit + " " +
                      "{:,}".format(int(percent_use)).rjust(10)
                      )


def remove_duplicates():
    common.print_line('removing duplicates')
    cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid ls command')
        usage_removedups()
        sys.exit(-1)
    cl_sync.remove_duplicates(common.remove_ending_slash(__args[1]))


def main(argv):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    read_args(argv)
    configure(__configfile)
    verify_configuration()
    logging.debug('config: ' + str(__config))

    print_heading()

    if __args[0] == 'ls':
        ls()
    elif __args[0] == 'lsmd5':
        lsmd5()
    elif __args[0] == 'backup':
        try:
            backup()
        except Exception as e:
            if __config['smtp_enable'] is True:
                logging.info('sending email')
                email = smtp_email.EMail()
                email.set_from(__config['smtp_from'])
                email.set_to(__config['smtp_to'])
                email.set_smtp_server(__config['smtp_server'])
                email.set_smtp_port(__config['smtp_port'])
                if 'smtp_user' in __config:
                    email.set_smtp_user(__config['smtp_user'])
                if 'smtp_password' in __config:
                    email.set_smtp_password(__config['smtp_password'])
                email.set_subject('Sprinkle Failure Notification')
                email.set_message('Sprinkle has experienced the following error:\n\n' + str(e) +
                                  '\n\nExamine logs for additional information')
                email.send()
            traceback.print_exc(file=sys.stderr)
    elif __args[0] == 'restore':
        restore()
    elif __args[0] == 'stats':
        stats()
    elif __args[0] == 'removedups':
        remove_duplicates()
    else:
        logging.error('invalid command')
        usage()
        sys.exit(-1)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
