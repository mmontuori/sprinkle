# A Guide to Sprinkle

This document contains a basic starting guide to use Sprinkle. It will guide you in setting up Sprinkle
volumes and how to backup/recover data.

## Install
This section describes the installations steps required to install Sprinkle for Windows and Linux.
Keep in mind that the actual steps might change based on your environment.

### Install RClone
The first thing to do is to install RClone. The best way to install RClone is by following the official
guide [here](https://rclone.org/install/).  
After the installation is complete, the following 2 commands,
for Windows and Linux should report the respective installed version:
##### for Windows:
```
C:\>rclone.exe --version
rclone v1.43.1
- os/arch: windows/amd64
- go version: go1.11
```
##### for Linux:
```
$ rclone --version
rclone v1.43
- os/arch: linux/amd64
- go version: go1.11
```
You may need to modify the PATH environment variable to make the command available to the system.
Consult the related operating system documentation on the different way to modify the PATH environment
variable if needed.  
Now that RClone is installed, let's proceed...

### Install Python 3
Sprinkle is developed in Python 3. This chapter describes how to setup Python for Windows and Linux. The
best way to install Python is by following the official documentation [here](https://www.python.org/doc/).
After the installation is completed, the following two commands will return the respective version.  
Make sure the installed version is at least 3.6 or later.
##### for Windows:
```
C:\>python --version
Python 3.6.5
```
##### for Linux:
```
$  python3 --version
Python 3.6.2
```

On Linux the actual command might be called **python3** due to compatibility and co-existemce with
version 2.

### Install Sprinkle and Dependencies
Now, we can install Sprinkle and the necessary dependencies by following the officiel guide
[here](https://mmontuori.github.io/sprinkle/).  
After the installation is complete, executing the following two commands will report Sprinkle's version
for the respective operating system:
##### for Windows:
```
C:\>python sprinkle.py --version
VERSION:
    1.0.0, module version: 1.0.0, rclone module version: 1.0.2
```
##### for Linux:
```
$  sprinkle.py --version
VERSION:
    1.0.0, module version: 1.0.0, rclone module version: 1.0.2
```
At this point, you can check prerequisites with the following command:
```
sprinkle.py --check-prereq
checking prerequisites, examine the error messages below...
**** PASSED! ****
```
If anything other than PASSES! is displayed, resolve the problem until the PASSED! message is displayed.

## Configure
Now, that everything is installed and functional. Let's proceed with the configuration of RClone and
Sprinkle.
### Configure RClone
Configuring RClone is probably the most complex item to perform.
##### for Windows:
```
C:\>rclone config
Current remotes:

Name                 Type
====                 ====
nasbackup            drive
nasbackup2           drive
nasbackup3           drive

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q>
```
##### for Linux:
```
$ rclone config
Current remotes:

Name                 Type
====                 ====
nasbackup            drive
nasbackup2           drive
nasbackup3           drive

e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q>
```

### Configure Sprinkle
As long as RClone is configured correctly with volumes, Sprinkle works out of the box, however,
Sprinkle can be configured by editing the file sprinkle.conf. The file that ships with sprinkle
has all default values assigned which work for most installations, however, it's possible that
values have to be tweaked for specific installations. All values in sprinkle.conf are commented.
For example, the **debug** value
##### sprinkle.conf debug value:
```
# run sprinkle in debug mode. Expect a lot of output
# value: true|false
# debug=false
```
##### in order to change the value:
```
# run sprinkle in debug mode. Expect a lot of output
# value: true|false
debug=true
```
This modification will set the debug value to true and output additional information that can be
used for development or troubleshooting.

## Verify
### Verify Sprinkle->RClone->Volumes Connections
To verify proper Sprinkle operation, use any commands, like the stats command:
##### for Windows:
```
C:\>python sprinkle.py --version
calculating total and free space...
REMOTE                          SIZE                 FREE      %FREE
=============== ==================== ==================== ==========
nasbackup:                       15G                   0G          1
nasbackup2:                      15G                   1G          7
nasbackup3:                      15G                   0G          3
--------------- -------------------- -------------------- ----------
total:                           45G                   1G          3
```
##### for Linux:
```
sprinkle.py stats
calculating total and free space...
REMOTE                          SIZE                 FREE      %FREE
=============== ==================== ==================== ==========
nasbackup:                       15G                   0G          1
nasbackup2:                      15G                   1G          7
nasbackup3:                      15G                   0G          3
--------------- -------------------- -------------------- ----------
total:                           45G                   1G          3
```

## Backup
### Backup a Directory via Sprinkle
To backup (sprinkle) a local directory over to clustered volumes, use:
##### for Windows:
```
C:\>rclone backup C:\dir_to_backup
```
##### for Linux:
```
$ rclone backup /dir_to_backup
```

## Restore
### Restore a Previously Backed up Directory via Sprinkle
To restore a previously backed up directory, use:
##### for Windows:
```
C:\>rclone restore C:/dir_to_backup c:/restore_here
```
##### for Linux:
```
$ rclone restore /dir_to_backup /restore_here
```

## List
### List Directory Content via Sprinkle
In order to list files located on a clustered volume use the following commands:
##### for Windows:
```
C:\>python sprinkle.py ls c:/dir_to_list
retrieving file list from: nasbackup:/dir_to_list/router1...
retrieving file list from: nasbackup2:/dir_to_list/router1...
retrieving file list from: nasbackup3:/dir_to_list/router1...
--- NAME                              SIZE MOD TIME            REMOTE
--- ---------------------------- --------- ------------------- ---------------
--- /dir_to_list/test.txt               15 2018-11-09:02:05:34 nasbackup2:
-d- /dir_to_list/router1                -1 2018-11-10:00:56:29 nasbackup2:
```
##### for Linux:
```
$ sprinkle-py ls /dir_to_list
retrieving file list from: nasbackup:/dir_to_list/router1...
retrieving file list from: nasbackup2:/dir_to_list/router1...
retrieving file list from: nasbackup3:/dir_to_list/router1...
--- NAME                              SIZE MOD TIME            REMOTE
--- ---------------------------- --------- ------------------- ---------------
--- /dir_to_list/test.txt               15 2018-11-09:02:05:34 nasbackup2:
-d- /dir_to_list/router1                -1 2018-11-10:00:56:29 nasbackup2:
```

## Help
### Built-in Help
Sprinkle comes with a very extensive built-in help. Any option can be used from as a command line
argument or set into the sprinkle.conf file. To invoke the built-in help use:
##### for Windows:
```
C:\>python sprinkle.py --help
NAME:
    sprinkle - the cloud clustered backup utility

SYNOPSIS:
    sprinkle.py [options} {command} {arg...arg}

DESCRIPTION:
    Sprinkle is a volume clustering utility. It presents all the RClone available volumes as a single clustered volume.
    It supports 1-way sync mainly for backup and recovery.
    Sprinkle uses the excellent [RClone](https://rclone.org) software for cloud volume access.

EXAMPLES:
    sprinkle.py ls /backup
    sprinkle.py backup /dir_to_backup
    sprinkle.py restore /backup /opt/restore_dir
    sprinkle.py stats
    sprinkle.py -c /home/sprinkle/sprinkle.conf ls /backup
...
...
```
##### for Linux:
```
$ sprinkle-py --help
NAME:
    sprinkle - the cloud clustered backup utility

SYNOPSIS:
    sprinkle.py [options} {command} {arg...arg}

DESCRIPTION:
    Sprinkle is a volume clustering utility. It presents all the RClone available volumes as a single clustered volume.
    It supports 1-way sync mainly for backup and recovery.
    Sprinkle uses the excellent [RClone](https://rclone.org) software for cloud volume access.

EXAMPLES:
    sprinkle.py ls /backup
    sprinkle.py backup /dir_to_backup
    sprinkle.py restore /backup /opt/restore_dir
    sprinkle.py stats
    sprinkle.py -c /home/sprinkle/sprinkle.conf ls /backup
...
...
```

## Contributing
Please read [CONTRIBUTING.md](https://mmontuori.github.io/sprinkle/docs/CONTRIBUTING) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning
We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors
* **Michael Montuori** - *Initial work* - [mmontuori](https://github.com/mmontuori)

## License
This project is licensed under the GPLv3 License - see the [LICENSE.md](https://github.com/mmontuori/sprinkle/LICENSE) file for details

