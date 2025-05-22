#!/usr/bin/env python3
from datetime import date, datetime, timedelta
import json
import os

def load_config():
    default = {
        "show_long_count": True,
        "show_tzolkin": True,
        "show_haab": True,
        "day_offset": 0,
        "sunrise_hour": 6  # fallback sunrise hour
    }
    config_path = os.path.expanduser("~/.local/share/cinnamon/applets/mayan-calendar@n1/config.json")
    try:
        with open(config_path, "r") as f:
            user_config = json.load(f)
            default.update(user_config)
    except:
        pass
    return default

def observed_day(config):
    now = datetime.now()
    sunrise_hour = config.get("sunrise_hour", 6)
    
    # If before sunrise, use yesterday
    if now.hour < sunrise_hour:
        return date.today() - timedelta(days=1)
    return date.today()

def mayan_date():
    config = load_config()
    offset = config.get("day_offset", 0)
    gregorian_date = observed_day(config) + timedelta(days=offset)

    # Julian Day Number
    jdn = gregorian_date.toordinal() + 1721424.5
    mayan_days = int(jdn - 584283)  # GMT correlation

    # Long Count
    baktun = mayan_days // 144000
    katun = (mayan_days % 144000) // 7200
    tun = (mayan_days % 7200) // 360
    uinal = (mayan_days % 360) // 20
    kin = mayan_days % 20 + 1

    # Tzolk'in
    tzolkin_names = [
        "Imix'", "Ik’", "Ak’b’al", "K’an", "Chikchan", "Kimi", "Manik’", "Lamat", "Muluk", "Ok",
        "Chuwen", "Eb'", "B’en", "Ix", "Men", "K’ib'", "Kab’an", "Etz’nab’", "Kawak", "Ajaw"
    ]
    tzolkin_number = ((mayan_days + 4) % 13) + 2
    index = ((mayan_days + 19) % 20 + 1) % 20
    tzolkin_name = tzolkin_names[index]

    # Haab’
    haab_months = [
        "Pop", "Wo", "Sip", "Sotz’", "Sek", "Xul", "Yaxk’in", "Mol", "Ch’en", "Yax", 
        "Sak’", "Keh", "Mak", "K’ank’in", "Muwan", "Pax", "K’ayab", "Kumk’u", "Wayeb"
    ]
    haab_day_in_year = (mayan_days + 348) % 365
    if haab_day_in_year >= 360:
        haab_day = haab_day_in_year - 360
        haab_month = 18
    else:
        haab_day = haab_day_in_year % 20
        haab_month = haab_day_in_year // 20
    haab_name = haab_months[haab_month]

    # Output formatting
    result = []
    if config.get("show_long_count", True):
        result.append(f"LC {baktun}.{katun}.{tun}.{uinal}.{kin}")
    if config.get("show_tzolkin", True):
        result.append(f"{tzolkin_name} {tzolkin_number}")
    if config.get("show_haab", True):
        result.append(f"{haab_name} {haab_day}")

    return ", ".join(result)

if __name__ == "__main__":
    print(mayan_date())

