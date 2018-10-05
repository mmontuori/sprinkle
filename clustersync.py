#!/usr/bin/env python
"""
clustersync main module

__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = []
__license__ = "closed"
__version__ = "0.1"
"""

from clsync import rclone
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

rclone = rclone.RClone("c:/Users/micha/.config/rclone/rclone.conf", "c:/utilities/rclone/rclone.exe")

remotes = rclone.get_remotes()

logging.debug('remotes: ' + str(remotes))

for remote in remotes:
    logging.debug('remote: ' + remote)
    #json = rclone.get_about(remote)
    #out = rclone.mkdir(remote, "/test")
    #out = rclone.rmdir(remote, "/test")
    #out = rclone.touch(remote, "/test.touch")
    #out = rclone.delete_file(remote, "/test.touch")
    #out = rclone.copy('c:/temp/nstest.blend', remote + "/nstest.blend")
    out = rclone.move('c:/temp/nstest.blend', remote + "/nstest.blend")

version = rclone.get_version()
