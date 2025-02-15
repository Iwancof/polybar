#!/bin/python3

import psutil
import netifaces
import toml
from netaddr import IPAddress

# load configuration
color_configs = toml.load("/home/iwancof/.config/polybar/colors.ini")['colors']

def dye(color: str, text: str) -> str:
    return f"%{{F{color_configs[color]}}}{text}%{{F-}}"

def underline(color: str, text: str) -> str:
    return f"%{{u{color_configs[color]}}}%{{+u}}{text}%{{u-}}%{{-u}}"

# get network interfaces
stats = psutil.net_if_stats()

available_interfaces = []

for (name, stat) in stats.items():
    if stat.isup and not "loopback" in stat.flags:
        available_interfaces.append(name)

# get network addresses
interface_addresses = psutil.net_if_addrs()
available_addresses = {}

for interface_name in available_interfaces:
    interface = interface_addresses[interface_name]

    v4 = next(filter(lambda x: x.family == netifaces.AF_INET, interface))

    available_addresses[interface_name] = {"ip": v4.address, "netmask": v4.netmask}

def dye_address(addr) -> str:
    ip = addr["ip"].split('.')
    netmask = addr["netmask"].split('.')

    result = []

    for ip, mask in zip(ip, netmask):
        # centered
        # ip = '*' * len(ip)

        if mask == "255":
            result.append(dye("network-part", ip))
        else:
            result.append(dye("host-part", ip))

    result = '.'.join(result)

    netmask = IPAddress(addr["netmask"])
    if netmask.is_netmask():
        cidr = IPAddress(addr["netmask"]).netmask_bits()
        result += "/"
        result += dye("network-part", str(cidr))

    address = IPAddress(addr["ip"])
    if address.is_global():
        result += " "
        result += dye("warning", "GLOBAL")

    return result

def dye_interface(interface) -> str:
    if interface == "wlan0":
        return dye("wi-fi", "wlan0")
    elif interface == "enp0s31f6":
        return dye("ethernet", "enp0s31f6")
    elif interface == "tailscale0":
        return dye("tailscale", "tailscale0")
    else:
        return dye("bar-foreground", interface)

result = []
for interface, addr in available_addresses.items():
    result.append(f"{dye_interface(interface)}({underline("active", dye_address(addr))})")

print(" ".join(result))
