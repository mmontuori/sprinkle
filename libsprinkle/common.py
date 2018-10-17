#!/usr/bin/env python3
"""
common utilities
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "2"

import subprocess
import os.path
import logging

def combine_jsons(json_str):
    return '[' + json_str.replace(']\n',',',json_str.count(']\n')-1).replace('||[\n','')

def is_file(file):
    if not os.path.isfile(file):
        return False
    else:
        return True

def is_dir(dir):
    if not os.path.isdir(dir):
        return False
    else:
        return True


def remove_localdir(local_dir, path):
    basedir = os.path.dirname(local_dir)
    return path.replace(basedir,'').replace('\\', '/')


def normalize_path(path):
    return path.replace('\\', '/')


def execute(command_with_args, no_error=False):
    logging.debug("Invoking : %s", " ".join(command_with_args))
    try:
        with subprocess.Popen(
                command_with_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE) as proc:
            (out, err) = proc.communicate()

            logging.debug(out)
            if err and no_error is False:
                logging.warning(err.decode("utf-8").replace("\\n", "\n"))

            return {
                "code": proc.returncode,
                "out": out.decode('utf-8'),
                "error": err.decode('utf-8')
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


def print_line(line):
    print(line)


def remove_ending_slash(path):
    if path.endswith('/'):
        logging.debug('removing ending slash from ' + path)
        return path[0:len(path)-1]
    else:
        return path


def convert_unit(amount, unit):
    if unit == 'G':
        return int(amount / 1024 / 1024 / 1024)
    if unit == 'M':
        return int(amount / 1024 / 1024)
    if unit == 'K':
        return int(amount / 1024)
    if unit == 'B':
        return amount

