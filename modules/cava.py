#!/bin/python3

import tempfile
import subprocess
import toml
import os

color_configs = toml.load("/home/iwancof/.config/polybar/colors.ini")['colors']

def dye(color: str, text: str) -> str:
    return f"%{{F{color_configs[color]}}}{text}%{{F-}}"

bars = [c for c in "▁▂▃▄▅▆▇█"]

bars[-2] = dye("cava-large", bars[-2])
bars[-1] = dye("cava-large", bars[-1])

num_bars = int(os.environ.get("NUM_BARS", 20))

fp = tempfile.NamedTemporaryFile()

fp.write(f"""
[general]
bars = {num_bars}

[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = {len(bars) - 1}

channels = mono

[smoothing]

noise_reduction = 0
""".encode())

fp.flush()

# spawn cava
cava = subprocess.Popen(["cava", "-p", fp.name], stdout=subprocess.PIPE)

# read from cava
while True:
    line = cava.stdout.readline().decode("utf-8").strip()
    if not line:
        print("AA")
        while True:
            pass

    values = list(map(int, line.split(";")[:-1]))

    result = ""
    for value in values:
        result += bars[value]

    print(result, flush=True)

