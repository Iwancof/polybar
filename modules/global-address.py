#!/bin/python3

import requests
import toml
import os
import geoip2.database

check_api = os.environ.get("CHECK_API", "https://api.ipify.org")

proxied = False
if os.environ.get("PROXYCHAINS_CONF_FILE"):
    proxied = True

color_configs = toml.load("/home/iwancof/.config/polybar/colors.ini")['colors']

def dye(color: str, text: str) -> str:
    return f"%{{F{color_configs[color]}}}{text}%{{F-}}"

def underline(color: str, text: str) -> str:
    return f"%{{u{color_configs[color]}}}%{{+u}}{text}%{{u-}}%{{-u}}"

def get_global_address():
    try:
        response = requests.get(check_api)
        return response.text
    except requests.RequestException:
        return ""

def get_location():
    with geoip2.database.Reader("/home/iwancof/.config/polybar/modules/GeoLite2-City.mmdb") as reader:
        global_address = get_global_address()
        if global_address:
            response = reader.city(global_address)
            return (global_address, response)
        else:
            return None

addr_location = get_location()
if addr_location is None:
    print(dye("critical", "Failed"))
else:
    global_address, location = addr_location
    result = []

    if location.country.name:
        result.append(dye("geoip-country", location.country.name))
    if location.city.name:
        result.append(dye("geoip-city", location.city.name))

    result = "-".join(result)

    # sensored ip address (all digits -> *)
    # global_address = ".".join(["*" * len(part) for part in global_address.split(".")])

    result = f"{global_address}({result})"

    if proxied:
        result = underline("geoip-proxied", result)

    print(result)

