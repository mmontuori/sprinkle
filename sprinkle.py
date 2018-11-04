#!/usr/bin/env python3
"""
libsprinkle main module
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "3"

from libsprinkle import clsync
from libsprinkle import rclone
from libsprinkle import config
from libsprinkle import common
from libsprinkle import smtp_email
import logging
import getopt
import sys
import traceback
import os


def print_heading():
    print("")
    print('sprinkle : the cloud clustered backup utility')


def copyrights():
    print('')
    print("(C)2018 Michael Montuori, [michael.montuori@gmail.com]. All rights reserved.")


def usage_options():
    print('')
    print("  options:")
    print("            -h|--help = help")
    print("            -c|--conf = configuration file")
    print("         -v|--version = print version")
    print("           -d|--debug = debug output")
    print("          --dist-type = distribution type (default:mas)")
    print("        --comp-method = compare method [size|md5] (default:size)")
    print("         --rclone-exe = rclone executable (default:rclone)")
    print("        --rclone-conf = rclone configuration (default:None)")
    print("       --display-unit = display unit [G|M|K|B]")
    print("            --retries = number of retries (default:1)")
    print("      --show-progress = show progress")
    print("       --delete-files = do not delete files on remote end (default:false)")
    print(" --restore-duplicates = restore files if duplicates are found (default:false)")
    print("            --dry-run = perform a dry run without actually backing up")
    print("           --no-cache = turn off caching")
    print("       --exclude-file = file containing the backup exclude paths")
    print("      --exclude-regex = regular expression to match for file backup exclusion **TBD**")


def usage_commands():
    print('')
    print("  commands:")
    print("                   ls = list files")
    print("                lsmd5 = list md5 of files")
    print("               backup = backup files to clustered drives")
    print("              restore = restore files from clustered drives")
    print("                stats = display volume statistics")
    print("           removedups = removes duplicate files")
    print("                 help = displays the help fot the specific command")


def usage():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options} {command} {arg...arg}")
    usage_commands()
    usage_options()
    copyrights()


def usage_ls():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options} ls {path}")
    print("       path = the remote path to list files")
    usage_options()
    copyrights()


def usage_lsmd5():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options] lsmd5 {path}")
    print("       path = the remote path to list md5")
    usage_options()
    copyrights()


def usage_backup():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options] backup {local dir}")
    print("  local dir = the local directory to backup")
    usage_options()
    copyrights()


def usage_restore():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options] restore {remote dir} {local dir}")
    print(" remote dir = the remote directory to restore")
    print("  local dir = the location where to store the restore")
    usage_options()
    copyrights()


def usage_help():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options] help {command}")
    print("    command = the command to display help for")


def usage_stats():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options] stats")
    usage_options()
    copyrights()


def usage_removedups():
    print_heading()
    version()
    print('')
    print("usage: sprinkle.py [options] removedups [path]")
    print("      path = the path to calculate duplicates")
    usage_options()
    copyrights()


def version():
    print("version: " + __version__ + '.' + __revision__ +
          ", module version: " + clsync.__version__ + '.' + clsync.__revision__ +
          ", rclone module version: " + rclone.__version__ + '.' + rclone.__revision__)


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
    global __restore_duplicates
    global __dry_run
    global __smtp_enable
    global __smtp_from
    global __smtp_to
    global __smtp_server
    global __smtp_port
    global __smtp_user
    global __smtp_password
    global __no_cache
    global __cl_sync
    global __exclude_file
    global __exclude_regex

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
    __restore_duplicates = False
    __dry_run = None
    __smtp_enable = None
    __smtp_from = None
    __smtp_to = None
    __smtp_server = None
    __smtp_port = None
    __smtp_user = None
    __smtp_password = None
    __no_cache = None
    __cl_sync = None
    __exclude_file = None
    __exclude_regex = None

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
                                    "restore-duplicates",
                                    "smtp-enable",
                                    "smtp-from=",
                                    "smtp-to=",
                                    "smtp-server=",
                                    "smtp-port=",
                                    "smtp-user=",
                                    "smtp-password=",
                                    "no-cache",
                                    "exclude-file=",
                                    "exclude-regex="
                                    ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-v', '--version'):
            version()
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
        elif opt in ("--restore-duplicates"):
            __restore_duplicates = True
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
        elif opt in ("--no-cache"):
            __no_cache = True
        elif opt in ("--exclude-file"):
            __exclude_file = arg
        elif opt in ("--exclude-regex"):
            __exclude_regex = arg

    if len(args) < 1:
        usage()
        sys.exit()

    __args = args


def configure(config_file):
    global __config

    _default_values = {
        "debug": False,
        "dry_run": False,
        "show_progress": False,
        "delete_files": False,
        "restore_duplicates": False,
        "smtp_enable": False,
        "no_cache": False,
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

    for field in _default_values:
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

    if __no_cache is not None:
        __config['no_cache'] = __no_cache

    if __exclude_file is not None:
        __config['exclude_file'] = __exclude_file

    if __exclude_regex is not None:
        __config['exclude_regex'] = __exclude_regex


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

    if 'exclude_file' in __config and __config['exclude_file'] is not None:
        if not os.path.isfile(__config['exclude_file']):
            raise Exception('exclude_file ' + __config['exclude_file'] + ' not found!')
        global __exclusion_list
        __exclusion_list = load_exclusion_file(__config['exclude_file'])
        logging.debug('exclusion list: ' + str(__exclusion_list))
        __config['__exclusion_list'] = __exclusion_list


def load_exclusion_file(exclude_file):
    logging.debug('loading exclusion file ' + exclude_file)
    lines = []
    with open(exclude_file, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.replace('\\', '/')
            lines.append(line)
        f.close()
    return lines


def init_logging(debug):
    if debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def ls():
    global __cl_sync
    if __cl_sync is None:
        __cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid ls command')
        usage_ls()
        sys.exit(-1)
    files = __cl_sync.ls(common.remove_ending_slash(__args[1]))
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
    global __cl_sync
    if __cl_sync is None:
        __cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid lsmd5 command')
        usage_lsmd5()
        sys.exit(-1)
    files = __cl_sync.lsmd5(common.remove_ending_slash(__args[1]))
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
    global __cl_sync
    if __cl_sync is None:
        __cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid backup command')
        usage_backup()
        sys.exit(-1)
    local_dir = common.remove_ending_slash(__args[1])
    common.print_line('backing up ' + local_dir + '...')
    __cl_sync.backup(local_dir, __config['delete_files'], __config['dry_run'])


def restore():
    global __cl_sync
    if __cl_sync is None:
        __cl_sync = clsync.ClSync(__config)
    if len(__args) < 3:
        logging.error('invalid remote command')
        usage_restore()
        sys.exit(-1)
    remote_path = __args[2]
    local_dir = common.remove_ending_slash(__args[1])
    if __config['restore_duplicates'] is False:
        common.print_line('checking if duplicates are present before restoring...')
        duplicates = __cl_sync.remove_duplicates(local_dir, True)
        if len(duplicates) > 0:
            common.print_line('DUPLICATE FILES FOUND:')
            for duplicate in duplicates:
                common.print_line("\t" + duplicate)
            common.print_line('restore cannot proceed! Use remove duplicates function before continuing')
            return
    common.print_line('restoring ' + remote_path + ' from ' + local_dir)
    __cl_sync.restore(local_dir, remote_path, __config['dry_run'])


def stats():
    global __cl_sync
    logging.debug('display stats about the volumes')
    common.print_line('calculating total and free space...')
    if __cl_sync is None:
        __cl_sync = clsync.ClSync(__config)
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
    sizes = __cl_sync.get_sizes()
    frees = __cl_sync.get_frees()
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

    size = __cl_sync.get_size()
    free = __cl_sync.get_free()
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
    global __cl_sync
    common.print_line('removing duplicates')
    if __cl_sync is None:
        __cl_sync = clsync.ClSync(__config)
    if len(__args) == 1:
        logging.error('invalid removedups command')
        usage_removedups()
        sys.exit(-1)
    __cl_sync.remove_duplicates(common.remove_ending_slash(__args[1]))


def main(argv):
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    read_args(argv)
    configure(__configfile)
    verify_configuration()
    logging.debug('config: ' + str(__config))

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
    elif __args[0] == 'help':
        if len(__args) < 2:
            usage_help()
        else:
            if __args[1] == 'ls':
                usage_ls()
            if __args[1] == 'lsmd5':
                usage_lsmd5()
            if __args[1] == 'backup':
                usage_backup()
            if __args[1] == 'restore':
                usage_restore()
            if __args[1] == 'stats':
                usage_stats()
            if __args[1] == 'removedups':
                usage_removedups()
            else:
                print('')
                print('invalid command. Use help [command]')
                sys.exit(-1)

        quit()
    else:
        print('')
        print('invalid command. Use help [command]')
        sys.exit(-1)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv[1:])
