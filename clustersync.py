from clsync import rclone
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

rclone = rclone.RClone("c:/Users/micha/.config/rclone/rclone.conf", "c:/utilities/rclone/rclone.exe")

remotes = rclone.get_remotes()

logging.debug('remotes: ' + str(remotes))

for remote in remotes:
    logging.debug('remote: ' + remote)
    lsjson = rclone.get_lsjson(remote, "/")

