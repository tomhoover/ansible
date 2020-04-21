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
            if not "--quiet" in args:
                subprocess.run(["echo", "\n#### ", host, ":", filesystem, " ---> ", myhost, ":", backup_store[myhost], "/", host, "/", filesystem, " ####\n"])
            if host == myhost:  # localhost
                sync_command = "syncoid %s --recursive --no-sync-snap --create-bookmark %s %s/%s/%s" % (args, filesystem, backup_store[myhost], host, filesystem)
            else:
                sync_command = "syncoid %s --recursive --no-sync-snap --create-bookmark root@%s:%s %s/%s/%s" % (args, host, filesystem, backup_store[myhost], host, filesystem)
            subprocess.run(sync_command.split())

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
