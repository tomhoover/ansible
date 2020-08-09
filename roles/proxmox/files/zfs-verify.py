#!/usr/bin/env python3

# ZFS: verify recent snapshot creation

import os
import sys
import time
import subprocess

MAX_SNAPSHOT_AGE = 24   # in hours

ignored_filesystems =   { "freenas": "",
                          "pvhost1": "external external/backups external/backups/dump external/backups/freenas external/backups/hass external/backups/pvhost1 external/backups/pvhost1/external external/backups/pvhost2 external/backups/pvhost3 external/backups/z_old external/backups/z_old/** external/bethel-image external/pve-backups external/pve-templates", 
                          "pvhost2": "backups backups/ariel-wl backups/arq backups/dump backups/duplicacy_backups backups/external backups/pvhost1 backups/pvhost1/external backups/pvhost2 backups/pvhost3 backups/pvhost3/pool backups/rsync backups/tar backups/unraid backups/unraid/** backups/z_old backups/z_old/** d14 d14/14 d15 d15/15 d16 d16/16 d17 d17/17 d18 d18/18 d19 d19/19 d20 d20/20 p1 p1/1 p25 p25/25", 
                          "pvhost3": "external external/backups external/backups/dump external/backups/freenas external/backups/hass external/backups/pvhost1 external/backups/pvhost1/external external/backups/pvhost2 external/backups/pvhost3 external/backups/z_old external/backups/z_old/** external/bethel-image external/pve-backups external/pve-templates" }

def filesystems():                  # list all zfs filesystems
    run_command = "zfs list -rH -o name"
    f = subprocess.run(run_command.split(), capture_output = True)
    f2 = f.stdout.decode('utf8').splitlines()
    return remove_ignored_filesystems(f2)

def remove_ignored_filesystems(filesystems):
    ign_fs = ignored_filesystems[myhost].split()
    for i in ign_fs:
        if os.isatty(sys.stdout.fileno()) and not "--quiet" in args:
            break
        elif not '**' in i:
            try:
                filesystems.remove(i);
            except ValueError:
                print("%s%s%s : %s%s%s" % (Blue, i, Default, Red, "Not found in ignored_filesystems dictionary", Default))
                break
        else:
            wildcard = i[:-2]
            fs_tmp = filesystems[:]
            for f in fs_tmp:
                if wildcard in f:
                    filesystems.remove(f);
    return (filesystems)

def snapshot_date(filesystem):
    """
    return zfs filesystem 'creation date' in the following format:
        Fri Apr 17 16:00 2020
    """
    run_command = "zfs list -H -o creation -t snapshot %s" % (filesystem)
    d = subprocess.run(run_command.split(), capture_output = True)
    list = d.stdout.decode('utf8').splitlines()
    if len(list) == 0:
        return "no datasets available"
    else:
        return list[len(list)-1]

# main

args = ""
myhost = os.uname()[1]
  
total = len(sys.argv)
if total >= 2:  # at least one argument has been passed
    args = " ".join(sys.argv[1:])

if os.isatty(sys.stdout.fileno()):
    Default = '\033[0m'  # reset to default text color
    Red     = '\033[31m' # set text color to red
    Green   = '\033[32m' # set text color to green
    Blue    = '\033[34m' # set text color to blue
else:
    Default = ''
    Red     = ''
    Green   = ''
    Blue    = ''

for filesystem in filesystems():
    sd = snapshot_date(filesystem)                                                  # Fri Apr 17 16:00 2020
    if sd == "no datasets available":
        print("%s%s%s : %s%s%s" % (Blue, filesystem, Default, Red, sd, Default))
    else:
        snapshot_datetime= time.mktime(time.strptime(sd, "%a %b %d %H:%M %Y"))      # Fri Apr 17 16:00 2020
        current_datetime= time.time()

        if current_datetime > snapshot_datetime + (MAX_SNAPSHOT_AGE * 60 * 60):    # convert MAX_SNAPSHOT_AGE to seconds before comparison
            print("%s%s%s : last snapshot was %s%s%s, which was more than %s hours ago" % (Blue, filesystem, Default, Red, sd, Default, str(MAX_SNAPSHOT_AGE)))
        else:
            if os.isatty(sys.stdout.fileno()) and not "--quiet" in args:
                print("%s%s%s : %s%s%s" % (Blue, filesystem, Default, Green, sd, Default))
