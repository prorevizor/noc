#!./bin/python
# ----------------------------------------------------------------------
# Change NOC's ip address
# ----------------------------------------------------------------------
# Copyright (C) 2007-2021 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import os
import sys
import socket
import fileinput

PG_VERSION = "9.6"


def get_my_ip():
    """Find out what ip address is lead to defroute interface"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
        print("Can't find proper IP interface")
    finally:
        s.close()
    return IP


def get_old_ip():
    """Read old ip from file from deploy"""
    try:
        ipfilepath = "/opt/noc/var/my_ip"
        with open('ipfilepath', 'r') as file:
            data = file.read()
    except EnvironmentError:
        print("No file with old IP")
        data = ""
    return data


def set_pg_address(address):
    """Set new IP to PostgreSQL"""
    deb_path = "/var/lib/postgresql/" + PG_VERSION + "/data/noc.conf"
    cent_path = "/var/lib/pgsql/" + PG_VERSION + "/data/noc.conf"
    for path in [deb_path, cent_path]:
        try:
            print(path)
            if os.path.isfile(path):
                for line in fileinput.input(files=path, inplace=True):
                    if line.strip().startswith('listen_addresses'):
                        line = "listen_addresses = \'" + address + "\'\n"
                    sys.stdout.write(line)
            return path
        except IOError:
            pass
    print('noc PG settings is not found')
    exit(1)


old_ip = get_old_ip()
print(old_ip)

my_ip = get_my_ip()
print(my_ip)

set_pg_address(my_ip)
command_for_restart_pg = "systemctl restart " + "postgresql-" + PG_VERSION
os.system(command_for_restart_pg)
