import requests
from datetime import datetime
import re
import time
import playsound
from prayertimehandler import PrayerTimeHandler
from audiofilehandler import play_audio

TIME_FORMAT = "%H:%M"
WAKEUP_TIME_BEFORE_SUNRISE = "00:30"
REGEX_MATCH = "0:00:00"


def get_current_time():
    now = datetime.now()
    current_time = now.strftime(TIME_FORMAT)
    return current_time


def get_prayer_times(city_name):
    url = f"https://dailyprayer.abdulrcs.repl.co/api/{city_name}"
    response = requests.get(url)
    data = response.json()
    # print(data['city'])
    # print(data['date'])
    prayer_time_list = []
    for prayer in data["today"]:
        prayer_time_list.append(data["today"][prayer])
        # print(prayer + ": " + data["today"][prayer])
    prayer_time_list = prayer_time_list[1:]  # removing Fajar start time
    return prayer_time_list
    # If you want to request for tomorrow prayer's time:
    # for prayer in data["tomorrow"]:
    #  print(prayer + ": " + data["tomorrow"][prayer])


def get_prayer_time_diff(prayer_times_list, current_time):
    prayer_diff_list = []
    for time in prayer_times_list:
        prayer_time = datetime.strptime(time, TIME_FORMAT)
        current_time_dt = datetime.strptime(current_time, TIME_FORMAT)
        diff = prayer_time - current_time_dt
        prayer_diff_list.append(str(diff))
    return prayer_diff_list


def main():
    city = "Ingolstadt"
    country = "Germany"
    while True:
        current_datetime = datetime.today()
        prayer_time_obj = PrayerTimeHandler(city, country, current_datetime.year)
        prayer_time_dict = prayer_time_obj.get_annual_prayer_times()
        prayer_times_list = prayer_time_obj.today_prayer_times(prayer_time_dict, current_datetime)
        # prayer_times_list = get_prayer_times("ingolstadt")
        current_time = get_current_time()
        prayer_times_list = prayer_time_obj.replace_sunrise_with_wakeup_time(prayer_times_list,
                                                                             WAKEUP_TIME_BEFORE_SUNRISE)
        prayer_time_diff = get_prayer_time_diff(prayer_times_list, current_time)
        print(f'_________________Current datetime : {current_datetime}_________________')
        for pr_time in prayer_time_diff:
            if re.match(REGEX_MATCH, pr_time):
                print("_______prayer_________")
                play_audio("")
                playsound.playsound("adan.mp3")
                time.sleep(120)
            else:
                print(pr_time)
        time.sleep(59)


if __name__ == "__main__":
    main()
