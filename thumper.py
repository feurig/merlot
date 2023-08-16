#!/usr/bin/python

import socket
import subprocess

def isExporting():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("thumper", 9100),timeout=3)
        if sock is not None:
            print('dew\'s dat wabbit')
            sock.close
        return True
    except OSError as e:
        pass
    return False
def kickThumper():
    ret = subprocess.call(["ssh", "root@henri-le-renne", "swctrl poe set auto id 6"]);
    ret = subprocess.call(["ssh", "root@henri-le-renne", "swctrl poe restart id 6"]);


if __name__ == '__main__':
    if (not isExporting()) :
        print("Thumpers not talking. Going to kick it")
        kickThumper()
