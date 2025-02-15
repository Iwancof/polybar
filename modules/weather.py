#!/bin/python3

import os
import json
import requests
import toml
from datetime import datetime, timedelta

# --- 色設定 ---
colors_config_path = "/home/iwancof/.config/polybar/colors.ini"
color_configs = toml.load(colors_config_path)['colors']

def dye(color_key: str, text: str) -> str:
    return f"%{{F{color_configs[color_key]}}}{text}%{{F-}}"

# --- Nerd Font 天気アイコン ---
weather_icons = {
    "Clear": "",          # 晴れ
    "Clouds": "",         # 曇り
    "Rain": "",           # 雨
    "Drizzle": "",        # 霧雨
    "Thunderstorm": "",   # 雷雨
    "Snow": "",           # 雪
    "default": ""         # その他
}

# --- 位置情報読み込み ---
RUNTIME_DIR = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
LOCATION_JSON = os.path.join(RUNTIME_DIR, "geo_location.json")

def load_location():
    try:
        with open(LOCATION_JSON, "r") as f:
            data = json.load(f)
            return data["lat"], data["lng"]
    except Exception as e:
        print("位置情報ファイルの読み込みに失敗しました:", e)
        return None, None

# --- Open-Meteo API 呼び出し ---
def get_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&"
        "hourly=weather_code&timezone=Asia%2FTokyo&forecast_days=1&models=jma_seamless"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Open-Meteo API の取得に失敗しました。")
        return None

# --- 天気コード対応表 & 判定 ---
weather_descriptions = {
    "0": "Clear sky",
    "1": "Mainly clear",
    "2": "Partly cloudy",
    "3": "Overcast",
    "45": "Fog",
    "48": "Depositing rime fog",
    "51": "Light drizzle",
    "53": "Moderate drizzle",
    "55": "Dense drizzle",
    "56": "Light freezing drizzle",
    "57": "Dense freezing drizzle",
    "61": "Slight rain",
    "63": "Moderate rain",
    "65": "Heavy rain",
    "66": "Light freezing rain",
    "67": "Heavy freezing rain",
    "71": "Slight snow fall",
    "73": "Moderate snow fall",
    "75": "Heavy snow fall",
    "77": "Snow grains",
    "80": "Slight rain showers",
    "81": "Moderate rain showers",
    "82": "Violent rain showers",
    "85": "Slight snow showers",
    "86": "Heavy snow showers",
    "95": "Thunderstorm",
    "96": "Thunderstorm with slight hail",
    "99": "Thunderstorm with heavy hail"
}

def categorize_weather(code: int) -> str:
    """天気コードをカテゴリに分類"""
    if code in [0, 1, 2, 3, 45, 48]:
        return "normal"
    elif code in [95, 96, 99]:
        return "critical"
    elif (51 <= code <= 57) or (61 <= code <= 67) or (71 <= code <= 77) or code in [80, 81, 82, 85, 86]:
        return "warning"
    else:
        return "normal"

def get_next_stormy(codes):
    """
    現在 normal のときに、次に 'warning' または 'critical' になるインデックスを探す。
    見つからなければ (None, None) を返す。
    """
    # i=1 から検索開始 (i=0 は「現在の天気」なのでスキップ)
    for i in range(1, len(codes)):
        cat = categorize_weather(codes[i])
        if cat in ["warning", "critical"]:
            return i, codes[i]
    return None, None

def get_next_stable(codes):
    """
    現在が warning/critical のときに、次に 'normal' になるインデックスを探す。
    見つからなければ (None, None) を返す。
    """
    for i in range(1, len(codes)):
        cat = categorize_weather(codes[i])
        if cat == "normal":
            return i, codes[i]
    return None, None

# --- 天気情報の整形 ---
def format_weather():
    lat, lon = load_location()
    if lat is None or lon is None:
        return "位置情報が取得できません。"

    weather_data = get_weather(lat, lon)
    if not weather_data:
        return "天気情報が取得できません。"

    # 現在の天気
    current = weather_data.get("current", {})
    current_temp = round(current.get("temperature_2m", 0))
    current_code = int(current.get("weather_code", -1))
    current_desc = weather_descriptions.get(str(current_code), "Unknown")
    current_cat = categorize_weather(current_code)

    # アイコンとカラーの選択
    if current_cat == "normal":
        color_key = "weather-normal"
        # 晴れアイコン or 曇りアイコン
        if current_code in [0, 1]:
            icon = weather_icons.get("Clear", weather_icons["default"])
        else:
            icon = weather_icons.get("Clouds", weather_icons["default"])
    elif current_cat == "warning":
        color_key = "weather-warning"
        # 雨 or 雪アイコン
        if (51 <= current_code <= 57) or (61 <= current_code <= 67):
            icon = weather_icons.get("Rain", weather_icons["default"])
        else:
            icon = weather_icons.get("Snow", weather_icons["default"])
    elif current_cat == "critical":
        color_key = "weather-critical"
        icon = weather_icons.get("Thunderstorm", weather_icons["default"])
    else:
        # 念のため
        color_key = "weather-normal"
        icon = weather_icons["default"]

    # 今からの予報(weather_code配列)を取得
    hourly = weather_data.get("hourly", {})
    codes = hourly.get("weather_code", [])

    # 次のイベント（荒れる or 安定）を検索
    next_time_info = ""
    if codes:
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        if current_cat == "normal":
            # 次に荒れるタイミング
            idx, next_code = get_next_stormy(codes)
            if idx is not None:
                cat = categorize_weather(next_code)
                desc = weather_descriptions.get(str(next_code), "Unknown")
                future_time = now + timedelta(hours=idx)
                time_str = future_time.strftime('%H:%M')
                # 'warning' or 'critical' で色を分ける
                next_color_key = "weather-warning" if cat == "warning" else "weather-critical"
                next_time_info = dye(next_color_key, f"[{time_str} {desc}]")
        else:
            # 現在が warning / critical -> 次に 'normal' (安定)
            idx, next_code = get_next_stable(codes)
            if idx is not None:
                desc = weather_descriptions.get(str(next_code), "Unknown")
                future_time = now + timedelta(hours=idx)
                time_str = future_time.strftime('%H:%M')
                # 安定した天気は 'weather-normal' で
                next_time_info = dye("weather-normal", f"[{time_str} {desc}]")

    # フォーマットして出力文字列を組み立て
    base_str = f"{icon}{current_desc}({current_temp}℃)"
    output = dye(color_key, base_str)
    if next_time_info:
        output += " " + next_time_info
    return output

if __name__ == "__main__":
    print(format_weather())

