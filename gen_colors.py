#!/bin/python3

import toml
import random

config = {}
config['colors'] = {}

# Raw colors
config['colors']['black'] = '#000000'
config['colors']['white'] = '#FFFFFF'
config['colors']['red'] = '#FF0000'
config['colors']['green'] = '#008000'
config['colors']['blue'] = '#0000FF'
config['colors']['lime'] = '#00FF00'
config['colors']['yellow'] = '#FFFF00'
config['colors']['cyan'] = '#00FFFF'
config['colors']['magenta'] = '#FF00FF'
config['colors']['gray'] = '#808080'
config['colors']['silver'] = '#C0C0C0'
config['colors']['maroon'] = '#800000'
config['colors']['navy'] = '#000080'
config['colors']['teal'] = '#008080'
config['colors']['olive'] = '#808000'
config['colors']['purple'] = '#800080'

config['colors']['light-red']     = '#FFA07A'  # ライトコーラル
config['colors']['light-green']   = '#90EE90'  # ライトグリーン
config['colors']['light-blue']    = '#ADD8E6'  # ライトブルー
config['colors']['light-yellow']  = '#FFFFE0'  # ライトイエロー
config['colors']['light-cyan']    = '#E0FFFF'  # ライトシアン
config['colors']['light-magenta'] = '#FF77FF'  # 仮のライトマゼンタ
config['colors']['light-gray']    = '#D3D3D3'  # ライトグレー
config['colors']['light-navy']    = '#6666FF'  # 仮のライトネイビー
config['colors']['light-teal']    = '#66CCCC'  # 仮のライトティール
config['colors']['light-purple']  = '#E6E6FA'  # ラベンダー（ライトパープル）

# apply random noise to original colors
noise_range = 20
for color in config['colors']:
    r_noise = random.randint(-noise_range, noise_range)
    g_noise = random.randint(-noise_range, noise_range)
    b_noise = random.randint(-noise_range, noise_range)
    color_hex = config['colors'][color]

    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:], 16)

    r = min(255, max(0, r + r_noise))
    g = min(255, max(0, g + g_noise))
    b = min(255, max(0, b + b_noise))

    config['colors'][color] = f'#{r:02x}{g:02x}{b:02x}'

# Basic colors
config['colors']['bar-background'] = config['colors']['black']
config['colors']['bar-foreground'] = config['colors']['white']

config['colors']['background'] = config['colors']['purple']

config['colors']['active'] = config['colors']['lime']
config['colors']['deactive'] = config['colors']['gray']

config['colors']['normal'] = config['colors']['light-green']
config['colors']['notice'] = config['colors']['cyan']
config['colors']['warning'] = config['colors']['yellow']
config['colors']['critical'] = config['colors']['red']

# For modules
config['colors']['charging'] = config['colors']['olive']
config['colors']['discharging'] = config['colors']['yellow']
config['colors']['full'] = config['colors']['green']
config['colors']['low'] = config['colors']['red']

config['colors']['cava-color'] = config['colors']['light-blue']
config['colors']['cava-large'] = config['colors']['light-red']

config['colors']['network-part'] = config['colors']['light-gray']
config['colors']['host-part'] = config['colors']['light-navy']

config['colors']['wi-fi'] = config['colors']['light-blue']
config['colors']['ethernet'] = config['colors']['light-green']
config['colors']['tailscale'] = config['colors']['yellow']

config['colors']['geoip-country'] = config['colors']['light-yellow']
config['colors']['geoip-city'] = config['colors']['light-cyan']
config['colors']['geoip-proxied'] = config['colors']['red']

config['colors']['time'] = config['colors']['bar-foreground']
config['colors']['date'] = config['colors']['gray']
config['colors']['weekday'] = config['colors']['gray']

config['colors']['geo-location'] = config['colors']['light-gray']

config['colors']['weather-normal'] = config['colors']['light-green']
config['colors']['weather-warning'] = config['colors']['yellow']
config['colors']['weather-critical'] = config['colors']['red']

# write as toml

with open('colors.ini', 'w') as f:
    toml.dump(config, f)
