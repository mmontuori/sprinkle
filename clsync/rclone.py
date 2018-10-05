
import logging
import subprocess
import os.path

class RClone:

    def __init__(self, config_file, rclone_exe="rclone"):
        logging.debug('constructing RClone')
        if config_file == None:
            logging.error("configuration file " + str(config_file) + " is None. Cannot continue!")
            raise Exception("None value for configuration file")
        if not os.path.isfile(config_file):
            logging.error("configuration file " + str(config_file) + " not found. Cannot continue!")
            raise Exception("Configuration file not found")
        if rclone_exe is not "rclone" and not os.path.isfile(rclone_exe):
            logging.error("rclone executable " + str(rclone_exe) + " not found. Cannot continue!")
            raise Exception("rclone executable not found")
        self._config_file = config_file
        self._rclone_exe = rclone_exe

    def _execute(self, command_with_args):
        logging.debug("Invoking : %s", " ".join(command_with_args))
        try:
            with subprocess.Popen(
                    command_with_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE) as proc:
                (out, err) = proc.communicate()

                # out = proc.stdout.read()
                # err = proc.stderr.read()

                logging.debug(out)
                if err:
                    logging.warning(err.decode("utf-8").replace("\\n", "\n"))

                return {
                    "code": proc.returncode,
                    "out": out.decode('ASCII'),
                    "error": err.decode('ASCII')
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

    def get_remotes(self):
        logging.debug('listing remotes')
        command_with_args = [self._rclone_exe, "listremotes", "--config", self._config_file]
        result = self._execute(command_with_args)
        logging.debug('result: ' + result['error'])
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        remotes = result['out'].splitlines()
        return remotes

    def get_lsjson(self, remote, directory):
        logging.debug('running lsjson for ' + remote + ":" + directory)
        command_with_args = [self._rclone_exe, "lsjson", "--config", self._config_file, remote+directory]
        result = self._execute(command_with_args)
        logging.debug('result: ' + str(result))
        if result['error'] is not '':
            logging.error('error getting remotes objects')
            raise Exception('error getting remote object. ' + result['error'])
        lsjson = result['out'].splitlines()
        logging.debug('returning ' + str(lsjson))
        return lsjson

