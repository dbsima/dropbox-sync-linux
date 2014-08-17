#!/usr/bin/python
import subprocess, time, re

print "Starting dropbox daemon"
print subprocess.check_output(['dropbox', 'start'])

started_sync = False
conseq_idle = 20
while True:
    status = subprocess.check_output(['dropbox', 'status'])
    print status
    if re.search("Updating|Indexing|Downloading", status):
        started_sync = True
        conseq_idle = 20
    elif re.search("Idle", status):
        conseq_idle-=1
        if not conseq_idle:
            if started_sync:
                print "Daemon reports idle consecutively after having synced. Stopping"
                time.sleep(5)
            else:
                print "Daemon seems to have nothing to do. Exiting"
            subprocess.call(['dropbox', 'stop'])
            break
    time.sleep(1)
