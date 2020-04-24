#!/usr/bin/env python3

# ZFS: replicate snapshots to backup server with syncoid

import os
import sys
import datetime
import subprocess

backup_store =        { "pvhost1": "external/backups", 
                        "pvhost2": "backups", 
                        "pvhost3": "" }
backup_filesystems =  { "ariel-wl": "tank",
                        "pvhost1": "rpool pool", 
                        "pvhost2": "rpool tank", 
                        "pvhost3": "rpool pool" }

def sync_it(host):
    if backup_store[myhost]:
        filesystems = backup_filesystems[host].split()
        for filesystem in filesystems:
            if host == myhost:  # localhost
                fs_check_command = "zfs list -H -o name %s" % (filesystem)
                sync_command = "syncoid %s --recursive --no-sync-snap --create-bookmark %s %s/%s/%s" % (args, filesystem, backup_store[myhost], host, filesystem)
            else:
                fs_check_command = "ssh %s zfs list -H -o name %s" % (host, filesystem)
                sync_command = "syncoid %s --recursive --no-sync-snap --create-bookmark root@%s:%s %s/%s/%s" % (args, host, filesystem, backup_store[myhost], host, filesystem)

            # verify backup_store is mounted
            bs_check_command = "zfs list -H -o name %s" % (backup_store[myhost])
            c = subprocess.run(bs_check_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not c.returncode == 0:       # if backup_store is not mounted, then break
                break

            # verify filesystem is mounted
            c = subprocess.run(fs_check_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if not c.returncode == 0:       # if filesystem is not mounted, then break
                break

            if not "--quiet" in args:
                subprocess.run(["echo", "\n#### ", host, ":", filesystem, " ---> ", myhost, ":", backup_store[myhost], "/", host, "/", filesystem, " ####\n"])

            c = subprocess.run(sync_command.split())
            # print(c)

# main

args = ""
myhost = os.uname()[1]

total = len(sys.argv)
if total >= 2:  # at least one argument has been passed
    args = " ".join(sys.argv[1:])

if not "--no-quiet" in args and str(datetime.datetime.now().hour) != '0' and not os.isatty(sys.stdout.fileno()):    # execute quietly if run via cron, except once daily or if '--no-quiet' arg is passed
    args = args + " --quiet"
else:
    args = args.replace('--no-quiet', '')

for host in backup_filesystems.keys():
    sync_it(host)
