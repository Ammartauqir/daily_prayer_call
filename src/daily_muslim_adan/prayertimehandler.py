import requests
import json
from os.path import exists

PRAYER_NAMES = ['Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'] # skipping 'Fajr' as adan only rings 30min before sunrise

class PrayerTimeHandler:
  def __init__(self, city, country, year):
    self.city = city
    self.country = country
    self.year = year
    self.timings_filename = f"annual_prayer_times_{city}_{year}.json"

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
      data = json.load(file)
    return data

def today_prayer_times(prayer_time_dict, current_date):
  month = current_date.month
  day = current_date.day
  todays_times = []
  for prayer in PRAYER_NAMES:
    time = prayer_time_dict["data"][str(month)][day]["timings"][prayer]
    time = time.split()[0]
    todays_times.append(time)
  return todays_times