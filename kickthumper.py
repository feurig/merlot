import socket
import subprocess

def isConnected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        sock = socket.create_connection(("thumper", 9100),timeout=10)
        if sock is not None:
            print('dew\'s dat wabbit')
            sock.close
        return True
    except OSError as e:
        pass
        ret = subprocess.call(["ssh", "root@henri-le-renne", "swctrl poe set off id 6"]);
    return False

isConnected()
