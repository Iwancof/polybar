#!/bin/python3

import toml
import os

color_configs = toml.load("/home/iwancof/.config/polybar/colors.ini")['colors']

def dye(color: str, text: str) -> str:
    return f"%{{F{color_configs[color]}}}{text}%{{F-}}"

def count_check_updates():
    updates = os.popen("checkupdates").read().split("\n")
    return len(updates) - 1

num = count_check_updates()

if num <= 10:
    color = "normal"
elif num <= 20:
    color = "notice"
elif num <= 50:
    color = "warning"
else:
    color = "critical"

print(dye(color, str(num)))
