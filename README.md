# Sprinkle (Volume Clustering)

Sprinkle is a volume clustering utility. It presents all the RClone available volumes as a single clustered volume. It supports 1-way sync mainly for
backup and recovery. Sprinkle uses the excellent [RClone](https://rclone.org) software for cloud access.

## Getting Started

The easiest way to install Sprinkle is via PyPI with:
```
pip3 install sprinkle-py
```

By cloning the repository to your running machine:
```
git clone https://gitlab.com/mmontuori/sprinkle.git
cd sprinkle
./sprinkle.py -c sprinkle.conf ls /
```

Via Snap:
```
sudo snap install sprinkle
```

## Prerequisites

* Python 3 installed
* RClone installed and available in the PATH or configured in sprinkle.conf file.
  [https://rclone.org](https://rclone.org) for reference.
* Few storage drives available from the supported RClone drives

## Installing

Following are the installation steps:

* GIT installed and access to [gitlab](https://gitlab.com)
* Download and install RCLone from [https://rclone.org](https://rclone.org)
* Run rclone config to configure and authorize your cloud or local storage
  (you might want to run the program on a machione for which http://localhost can be reached
  ideally, from your local workstation)
* Verify access to the storage by issuing the command "rclone ls alias:"
* Copy rclone.conf on the machine which will execute Sprinkle
* Download sprinkle from [https://someplace.com](https://someplace.com)
* Unzip the files into a location of your choice
* Make sure the prerequisites are satisfied
* From Sprinkle installation directory run "./sprinkle.py -c {path to sprinkle.conf} ls /"

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
./sprinkle.py {command} --help
```

## Authors

* **Michael Montuori** - *Head developer* - [mmontuori](https://gitlab.com/mmontuori)

## License

This project is licensed under the GPLv3 License - see the
[LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) file for details

## Acknowledgments

* Warren Crigger for development support
