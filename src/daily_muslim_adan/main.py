from datetime import datetime
import os
import time
import logging
from handlers.prayertimehandler import (
    PrayerTimeHandler,
    replace_sunrise_with_wakeup_time,
    get_next_prayer_diff_in_sec,
    convert_seconds,
)
from handlers.oledhandler import display_next_adan_name_time
from icecream import ic
from handlers.audiofilehandler import AudioPlayer

WAKEUP_TIME_BEFORE_SUNRISE = "00:30:00"
REGEX_MATCH = "0:00:00"
ADAN_AUDIO_FILE_PATH = os.path.abspath(os.path.join("src", "daily_muslim_adan", "data", "adan2.wav"))

def init_logging():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")


def main():
    city = "Ingolstadt"
    country = "Germany"
    player = AudioPlayer()
    current_year = datetime.today().year
    prayer_time_obj = PrayerTimeHandler(city, country, current_year)
    while True:
        current_datetime = datetime.now()
        today_prayer_times = prayer_time_obj.today_prayer_times(current_datetime)
        today_adan_times = replace_sunrise_with_wakeup_time(today_prayer_times, WAKEUP_TIME_BEFORE_SUNRISE)
        next_adan_name, next_adan_time_in_sec = get_next_prayer_diff_in_sec(today_adan_times)
        ic(next_adan_name)
        ic(next_adan_time_in_sec)
        ic(today_adan_times[next_adan_name])
        display_next_adan_name_time(
            next_adan_name,
            today_adan_times[next_adan_name],
            convert_seconds(next_adan_time_in_sec)
        )
        if next_adan_time_in_sec < 2:
            player.play_audio(ADAN_AUDIO_FILE_PATH)
        time.sleep(1)


if __name__ == "__main__":
    main()
