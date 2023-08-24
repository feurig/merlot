#!/usr/bin/python
#------------------------------------------------------------------- thumper.py
# Check the backyard temperature sensors  
#
# (C) D Delmar Davis 2023 
#
# Note: POC lots of hard coded foo here....
# it takes about a minute and 20 seconds to come back so..
# bunnyfoofoo's crontab should look like this
# */2 * * * * /usr/local/bin/thumper.py

import socket
import subprocess

#---------------------------------------------------------------- isExporting()
# Check to see if node exporter is running on thumper.
#
def isExporting():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("thumper", 9100),timeout=3)
        if sock is not None:
            print('Found da wabbit')
            sock.close
        return True
    except OSError:
        pass
    return False

#---------------------------------------------------------------- kickThumper()
# Make sure the poe port is on and powercycle that port
#
# https://www.devwithimagination.com/2022/08/07/restarting-poe-via-ssh-on-a-usw-lite-16-poe/

def kickThumper():
    ret = subprocess.call(["ssh",
                            "root@henri-le-renne",
                            "swctrl poe set auto id 6"]);
    ret = subprocess.call(["ssh", 
                           "root@henri-le-renne",
                           "swctrl poe restart id 6"]);


#------------------------------------------------------------------- __main__()
# Check to see if thumper is exporting and if not reset.
#
if __name__ == '__main__':
    if (not isExporting()) :
        print("Thumpers not talking. Going to kick it")
        kickThumper()
