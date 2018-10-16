# Sprinkle

Sprinkle is a volume clustering utility based on [RClone](https://rclone.org). It presents all the
RClone available volumes as a single clustered volume. It supports 1-way sync mainly for
backup and recovery.

## Getting Started

Get started by quickly cloning the repository to your running machine:

```
git clone https://gitlab.com/mmontuori/sprinkle.git
cd sprinkle
./sprinkle.py -c sprinkle.conf ls /
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

## Authors

* **Michael Montuori** - *Head developer* - [mmontuori](https://gitlab.com/mmontuori)

## License

This project is licensed under the GPLv3 License - see the
[LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) file for details

## Acknowledgments

* Warren Crigger for development support
