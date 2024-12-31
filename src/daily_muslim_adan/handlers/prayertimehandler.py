import requests
import json
from datetime import datetime
import os
from os.path import exists

PRAYER_NAMES = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']  # skipping 'Fajr' as adan only rings 30min before sunrise
PRAYER_FILE_PATH = "daily_muslim_adan/data/prayertime_files"
TIME_FORMAT = "%H:%M"


def replace_sunrise_with_wakeup_time(prayer_times_list, WAKEUP_TIME_BEFORE_SUNRISE):
    wakeup_time = datetime.strptime(prayer_times_list[0], TIME_FORMAT) - datetime.strptime(
        WAKEUP_TIME_BEFORE_SUNRISE,
        TIME_FORMAT)
    wakeup_time = str(wakeup_time)[:-3]
    prayer_times_list[0] = wakeup_time
    return prayer_times_list


class PrayerTimeHandler:
    def __init__(self, city, country, year):
        self.annual_prayer_data = None
        self.city = city
        self.country = country
        self.year = year
        self.timings_filename = os.path.join(PRAYER_FILE_PATH, f"annual_prayer_times_{city}_{year}.json")
        self.get_annual_prayer_times()

    def download_annual_prayer_calander(self):
        api_url = f'https://api.aladhan.com/v1/calendarByCity?city={self.city}&country={self.country}&method=1&annual=true&year={self.year}'
        response_API = requests.get(api_url)
        print(response_API.status_code)
        data = response_API.json()
        with open(self.timings_filename, "w") as write:
            json.dump(data, write)

    def get_annual_prayer_times(self):
        if not exists(self.timings_filename):
            self.download_annual_prayer_calander()
        with open(self.timings_filename, 'r') as file:
            self.annual_prayer_data = json.load(file)

    def today_prayer_times(self, current_date):
        month = current_date.month
        day = current_date.day
        today_times = []
        for prayer in PRAYER_NAMES:
            time = self.annual_prayer_data["data"][str(month)][day]["timings"][prayer]
            time = time.split()[0]
            today_times.append(time)
        return today_times


def get_current_time():
    current_time = datetime.now().strftime(TIME_FORMAT)
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
