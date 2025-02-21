#!/bin/python3

import toml
import random
import colorsys

def hex_to_rgb(hex_color: str):
    """ #RRGGBB 形式の文字列を (R, G, B) タプルにして返す(0~255)。 """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb: tuple):
    """ (R, G, B) タプル(0~255)を #RRGGBB 形式の文字列にして返す。 """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def apply_hsv_noise(hex_color: str, 
                    hue_noise_range=0.02, 
                    sat_noise_range=0.05, 
                    val_noise_range=0.05) -> str:
    """
    HSV空間でわずかにランダマイズを加えた色を返す。
      - hue_noise_range: 色相に加える乱数の最大幅 (0.02 -> ±0.02 = ±2%)
      - sat_noise_range: 彩度
      - val_noise_range: 明度
    """
    # RGB(0~255)に変換
    r, g, b = hex_to_rgb(hex_color)
    # 0~1に正規化
    r_f, g_f, b_f = r/255.0, g/255.0, b/255.0

    # colorsysでHSVに変換
    h, s, v = colorsys.rgb_to_hsv(r_f, g_f, b_f)

    # ランダムにオフセットを適用 (一部だけ変えたいなら、±範囲内で変動)
    h += random.uniform(-hue_noise_range, hue_noise_range)
    s += random.uniform(-sat_noise_range, sat_noise_range)
    v += random.uniform(-val_noise_range, val_noise_range)

    # 値を 0.0～1.0 でクリップする
    h = h % 1.0  # hueは1.0を超えたらループするので mod 1.0
    s = min(1.0, max(0.0, s))
    v = min(1.0, max(0.0, v))

    # RGBに戻す
    r_out, g_out, b_out = colorsys.hsv_to_rgb(h, s, v)
    # 0~255へ戻して丸め
    r_i, g_i, b_i = int(r_out*255), int(g_out*255), int(b_out*255)

    return rgb_to_hex((r_i, g_i, b_i))


def main():
    config = {}
    config['colors'] = {}

    # より視認性や区別を重視した色を定義（拡張版）。
    # 適宜、好みのカラーセットなどに変更してもOKです。
    # --------------------------------------------------
    config['colors']['black']       = '#000000'
    config['colors']['white']       = '#FFFFFF'
    config['colors']['gray']        = '#808080'
    config['colors']['silver']      = '#C0C0C0'
    config['colors']['light-gray']  = '#D3D3D3'
    
    # ベースカラー（ブルー系、オレンジ系など ）
    config['colors']['red']         = '#FF4136'
    config['colors']['blue']        = '#0074D9'
    config['colors']['green']       = '#2ECC40'
    config['colors']['yellow']      = '#FFDC00'
    config['colors']['orange']      = '#FF851B'
    config['colors']['purple']      = '#B10DC9'
    config['colors']['teal']        = '#39CCCC'
    config['colors']['maroon']      = '#85144B'
    config['colors']['olive']       = '#3D9970'
    config['colors']['navy']        = '#001F3F'

    # ライト系カラー（淡い色、背景などに）
    config['colors']['light-red']       = '#FFA07A'  # LightSalmon
    config['colors']['light-blue']      = '#ADD8E6'  # LightBlue
    config['colors']['light-green']     = '#90EE90'  # LightGreen
    config['colors']['light-yellow']    = '#FFFFE0'  # LightYellow
    config['colors']['light-cyan']      = '#E0FFFF'  
    config['colors']['light-magenta']   = '#FF77FF'  
    config['colors']['light-navy']      = '#6666FF'  
    config['colors']['light-teal']      = '#66CCCC'  
    config['colors']['light-purple']    = '#E6E6FA'  # Lavender
    config['colors']['light-orange']    = '#FFDAB9'  # PeachPuff
    
    # ノイズを加える範囲（例: 色相±3%、彩度±7%、明度±7% など）
    hue_noise_range = 0.03
    sat_noise_range = 0.07
    val_noise_range = 0.07

    # 色ごとにHSVノイズを適用
    for color_name, hex_color in config['colors'].items():
        noisy_color = apply_hsv_noise(
            hex_color, 
            hue_noise_range=hue_noise_range, 
            sat_noise_range=sat_noise_range, 
            val_noise_range=val_noise_range
        )
        config['colors'][color_name] = noisy_color

    # よく使う主要な色指定（bar背景、foreground など）
    config['colors']['bar-background'] = config['colors']['black']
    config['colors']['bar-foreground'] = config['colors']['white']

    # ウィンドウ・背景等
    config['colors']['background'] = config['colors']['purple']
    config['colors']['active']    = config['colors']['blue']
    config['colors']['deactive']  = config['colors']['gray']

    # ステータスレベル的な色
    config['colors']['normal']   = config['colors']['light-green']
    config['colors']['notice']   = config['colors']['cyan'] if 'cyan' in config['colors'] else '#00FFFF'
    config['colors']['warning']  = config['colors']['yellow']
    config['colors']['critical'] = config['colors']['red']

    # バッテリー状態など
    config['colors']['charging']     = config['colors']['olive']
    config['colors']['discharging']  = config['colors']['orange']
    config['colors']['full']         = config['colors']['green']
    config['colors']['low']          = config['colors']['red']

    # ビジュアライザ (cava) 
    config['colors']['cava-color'] = config['colors']['light-blue']
    config['colors']['cava-large'] = config['colors']['light-red']

    # ネットワーク系
    config['colors']['network-part'] = config['colors']['light-gray']
    config['colors']['host-part']    = config['colors']['light-navy']


    config['colors']['wi-fi']        = config['colors']['light-blue']
    config['colors']['ethernet']     = config['colors']['light-green']
    config['colors']['tailscale']    = config['colors']['yellow']

    # GeoIP
    config['colors']['geoip-country'] = config['colors']['light-yellow']
    config['colors']['geoip-city']    = config['colors']['light-cyan']
    config['colors']['geoip-proxied'] = config['colors']['red']

    # 時計表示
    config['colors']['time']    = config['colors']['bar-foreground']
    config['colors']['date']    = config['colors']['gray']
    config['colors']['weekday'] = config['colors']['gray']

    # 天気
    config['colors']['geo-location']     = config['colors']['light-gray']

    config['colors']['weather-normal']   = config['colors']['light-green']
    config['colors']['weather-warning']  = config['colors']['yellow']
    config['colors']['weather-critical'] = config['colors']['red']

    # TOML形式でファイル出力
    with open('colors.ini', 'w') as f:
        toml.dump(config, f)


if __name__ == "__main__":
    main()

