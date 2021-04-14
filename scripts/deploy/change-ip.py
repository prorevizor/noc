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
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
        print("Can't find proper IP interface")
    finally:
        s.close()
    return ip


def set_pg_address(address):
    """Set new IP to PostgreSQL"""
    deb_path = "/etc/postgresql/" + PG_VERSION + "/main/noc.conf"
    cent_path = "/var/lib/pgsql/" + PG_VERSION + "/data/noc.conf"
    for path in [deb_path, cent_path]:
        try:
            print(path)
            if os.path.isfile(path):
                for line in fileinput.input(files=path, inplace=True):
                    if line.strip().startswith("listen_addresses"):
                        line = "listen_addresses = '" + address + "'\n"
                    sys.stdout.write(line)
        except IOError:
            pass
    print("noc PG settings is not found")
    exit(1)


def set_consul_address(address):
    """Set new IP to Consul"""
    deb_path = "/etc/consul/config.json"
    for path in [deb_path]:
        try:
            print(path)
            if os.path.isfile(path):
                for line in fileinput.input(files=path, inplace=True):
                    if line.startswith("  \"bind_addr\""):
                        line = "\"bind_addr\": \"" + address + "\",\n"
                    sys.stdout.write(line)
        except IOError:
            pass
    print("Consul settings is not found")
    exit(1)


def set_mongo_address(address):
    """Set new IP to MongoDB"""
    deb_path = "/etc/mongod.conf"
    for path in [deb_path]:
        try:
            print(path)
            if os.path.isfile(path):
                for line in fileinput.input(files=path, inplace=True):
                    if line.strip().startswith("bindIp: 127.0.0.1,"):
                        line = "  bindIp: 127.0.0.1," + address + "\n"
                    sys.stdout.write(line)
        except IOError:
            pass
    print("MongoDB settings is not found")


def get_old_ip():
    """Read old ip from file from /etc/hosts"""
    try:
        ipfilepath = "/etc/hosts"
        with open(ipfilepath, "r") as file:
            hostname = socket.gethostname()
            for line in file.readlines():
                if line.strip().endswith(hostname):
                    old_address = line.split()[0]
                    return old_address
    except EnvironmentError:
        print("No file with old IP")


def set_hosts_address(address):
    """Set new IP to /etc/hosts"""
    deb_path = "/etc/hosts"
    for path in [deb_path]:
        try:
            print(path)
            if os.path.isfile(path):
                hostname = socket.gethostname()
                print(hostname)
                for line in fileinput.input(files=path, inplace=True):
                    if line.strip().endswith(hostname):
                        line = address + " " + hostname + "\n"
                    sys.stdout.write(line)
        except IOError:
            pass
    print("You haven't /etc/hosts")


def set_liftbridge_address(address):
    """Set new IP to Liftbridge"""
    deb_path = "/etc/liftbridge/liftbridge.yml"
    for path in [deb_path]:
        try:
            print(path)
            if os.path.isfile(path):
                for line in fileinput.input(files=path, inplace=True):
                    if line.strip().startswith("host: "):
                        line = "host: " + address + "\n"
                    if line.strip().startswith("- nats://"):
                        line = "- nats://" + address + ":4222\n"
                    sys.stdout.write(line)
        except IOError:
            pass
    print("Liftbridge settings is not found")


def change_nats_address(old_ip, new_ip):
    """Set new IP to Nats"""
    deb_path = "/etc/nats/nats-server.conf"
    for path in [deb_path]:
        try:
            print(path)
            if os.path.isfile(path):
                for line in fileinput.input(files=path, inplace=True):
                    line.replace(old_ip, new_ip)
                    sys.stdout.write(line)
        except IOError:
            pass
    print("Liftbridge settings is not found")


if __name__ == "__main__":
    old_ip_address = get_old_ip()
    print("Old ip was: ", old_ip_address)

    my_ip = get_my_ip()
    print("Local ip is: ", my_ip)

    change_nats_address(old_ip_address, my_ip)

    set_liftbridge_address(my_ip)
    os.system("systemctl restart liftbridge")

    set_pg_address(my_ip)
    os.system("systemctl restart postgresql")

    set_hosts_address(my_ip)

    set_consul_address(my_ip)
    os.system("systemctl restart consul")

    set_mongo_address(my_ip)
    os.system("systemctl restart mongod")
