#!/bin/python3

import subprocess
import toml

# load configuration
color_configs = toml.load("/home/iwancof/.config/polybar/colors.ini")['colors']

def dye(color: str, text: str) -> str:
    return f"%{{F{color_configs[color]}}}{text}%{{F-}}"

unsafe = ["󰤫", "󰤠", "󰤣", "󰤦", "󰤩"]
open   = ["󱛏", "󱛋", "󱛌", "󱛍", "󱛎"]
lock   = ["󰤬", "󰤡", "󰤤", "󰤧", "󰤪"]

# nmcli -t -f ACTIVE,SSID,SIGNAL,SECURITY device wifi list | grep yes

def get_wifi_info():
    try:
        output = subprocess.check_output(["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL,SECURITY", "device", "wifi", "list"]).decode("utf-8")
        output = output.split("\n")
        output = next(filter(lambda x: x.split(":")[0] == "yes", output))
        
        ssid, signal, security = output.split(":")[1:]
        return (ssid, signal, security)
    except subprocess.CalledProcessError:
        return []

(ssid, signal, security) = get_wifi_info()
signal = int(signal)

# based on https://fossies.org/linux/NetworkManager/src/nmcli/devices.c:80

if 80 < signal:
    signal_index = 4
elif 55 < signal:
    signal_index = 3
elif 30 < signal:
    signal_index = 2
elif 5 < signal:
    signal_index = 1
else:
    signal_index = 0

critical = False
warning = False

if signal_index < 3:
    warning = True
if signal_index < 1:
    critical = True

icons = lock
msg = "SAFE"
if security == "":
    critical = True
    icons = open
    msg = "FREE"
if "WEP" in security:
    critical = True
    icons = unsafe
    msg = "WEP "
if "WPA1" in security:
    warning = True
    icons = unsafe
    msg = "WPA1"

color = "normal"
if critical:
    color = "critical"
elif warning:
    color = "warning"

# censored
# ssid = "SSID-CENSORED"

print(f"{dye(color, ssid)}({dye(color, icons[signal_index])} {dye(color, msg)})")
