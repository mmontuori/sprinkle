# Sprinkle (Volume Clustering)

Sprinkle is a volume clustering utility. It presents all the RClone available volumes as a single clustered volume. It supports 1-way sync mainly for
backup and recovery. Sprinkle uses the excellent [RClone](https://rclone.org) software for cloud volume access.

Features:
* Consolidate multiple cloud drives into a single virtual drive
* Sprinkle your backup across multiple cloud drives
* Minimize cost by stacking multiple free cloud drives into single one
* Run as Unix daemon with custom schedules for seamless backups of important files
* Developed in Python for extreme multi-platform flexibility

## Getting Started

The easiest way to install Sprinkle and all prerequisites is via PyPI with:
```
pip3 install sprinkle-py
```

Or by cloning the repository to your running machine, but make sure prerequisites are met:
```
git clone https://gitlab.com/mmontuori/sprinkle.git
cd sprinkle
./sprinkle.py -c sprinkle.conf ls /
```
A more comprehensive guide can be found [here](https://mmontuori.github.io/sprinkle/docs/guide)

## Prerequisites

* Python 3 installed
* FileLock Python library [https://pypi.org/project/filelock](https://pypi.org/project/filelock)
* Progress Python library [https://pypi.org/project/progress](https://pypi.org/project/progress)
* RClone installed and available in the PATH or configured in sprinkle.conf file. RClone documentation
is available [here](https://rclone.org) for reference
* Few storage drives available from the supported RClone drives

## Installing

Following are the installation steps:

* Install Sprinkle with a supported method
* Download and install RCLone from [https://rclone.org](https://rclone.org)
* Run **RClone** config to configure and authorize your cloud or local storage
  (you might want to run the program on a machione for which http://localhost can be reached
  ideally, from your local workstation)
* Verify access to the storage by issuing the command "rclone ls {alias name}:"
* Copy rclone.conf on the machine which will execute Sprinkle
* Make sure all the prerequisites are satisfied
* Add **RClone** executable to the system PATH variable, or configure location in sprinkle.conf file
* From Sprinkle installation directory run **"./sprinkle.py [-c path to sprinkle.conf] ls /"**

From this point, backups and restore can be executed on the clustered storage.

```
./sprinkle.py -c {path to sprinkle.conf} backup {directory to backup}
```

Use the builtin --help utility to get additional commands and information.

```
./sprinkle.py --help
```

and the command specific help.

```
./sprinkle.py help {command}
```

## Authors

* **Michael Montuori** - *Head developer* - [mmontuori](https://gitlab.com/mmontuori)

## License

This project is licensed under the GPLv3 License - see the
[LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) file for details

## Acknowledgments

* Warren Crigger for development support
