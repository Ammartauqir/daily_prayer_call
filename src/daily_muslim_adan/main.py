from datetime import datetime
import os
import time
import logging
from handlers.prayertimehandler import (
    PrayerTimeHandler,
    get_current_time,
    replace_sunrise_with_wakeup_time,
    get_prayer_time_diff,
    get_next_prayer_diff_in_sec,
)
from handlers.oledhandler import display_current_time_date
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
        display_current_time_date(current_datetime)
        today_prayer_times = prayer_time_obj.today_prayer_times(current_datetime)
        today_adan_times = replace_sunrise_with_wakeup_time(today_prayer_times, WAKEUP_TIME_BEFORE_SUNRISE)
        next_adan_name, next_adan_time_in_sec = get_next_prayer_diff_in_sec(today_adan_times)
        ic(next_adan_name)
        ic(next_adan_time_in_sec)
        ic(today_adan_times[next_adan_name])

        if next_adan_time_in_sec < 1650:
            player.play_audio(ADAN_AUDIO_FILE_PATH)
        # next_adan_remaining_time = str(next_adan_time_diff).split(".")[0]  # Remove microseconds
        # print(f"\rTime left: {next_adan_remaining_time}", end="", flush=True)

        # prayer_time_diff = get_prayer_time_diff(prayer_times_list, get_current_time())
        # print(f'_________________Current datetime : {current_datetime}_________________')

        # for pr_time in prayer_time_diff:
        #     if re.match(REGEX_MATCH, pr_time):
        #         print("_______prayer_________")
        #         # play_audio("adan2.mp3")
        #     else:
        #         print(pr_time)
        time.sleep(1)


if __name__ == "__main__":
    main()
