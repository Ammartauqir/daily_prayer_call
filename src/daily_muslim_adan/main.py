import requests
from datetime import datetime
import re
import time
import playsound
from handlers.prayertimehandler import \
    PrayerTimeHandler, \
    get_current_time, \
    get_prayer_times, \
    get_prayer_time_diff
from handlers.audiofilehandler import play_audio

WAKEUP_TIME_BEFORE_SUNRISE = "00:30"
REGEX_MATCH = "0:00:00"


def main():
    city  = "Ingolstadt"
    country = "Germany"
    play_audio("adan.mp3")
    print("xxxxxxxxxxxxx")
    current_year = datetime.today().year
    prayer_time_obj = PrayerTimeHandler(city, country, current_year)
    while True:
        current_datetime = datetime.today()
        prayer_times_list = prayer_time_obj.today_prayer_times(current_datetime)
        current_time = get_current_time()
        # prayer_times_list = prayer_time_obj.replace_sunrise_with_wakeup_time(prayer_times_list,
        #                                                                      WAKEUP_TIME_BEFORE_SUNRISE)
        prayer_time_diff = get_prayer_time_diff(prayer_times_list, current_time)
        print(f'_________________Current datetime : {current_datetime}_________________')
        for pr_time in prayer_time_diff:
            if re.match(REGEX_MATCH, pr_time):
                print("_______prayer_________")
                play_audio("adan.mp3")
            else:
                print(pr_time)
        time.sleep(28)


if __name__ == "__main__":
    main()
