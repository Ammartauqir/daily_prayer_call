import requests
from datetime import datetime
import re
import time
from pydub import AudioSegment
from pydub.playback import play


TIME_FORMAT = "%H:%M"
WAKEUP_TIME_BEFORE_SUNRISE = "00:30"
REGEX_MATCH = "(0:00:00)|(0:01:00)|(0:02:00)|(2:23:00)"

def get_current_time():
  now = datetime.now()
  current_time = now.strftime(TIME_FORMAT)
  return current_time

def replace_sunrise_with_wakeup_time(prayer_times_list, WAKEUP_TIME_BEFORE_SUNRISE):
  wakeup_time = datetime.strptime(prayer_times_list[0], TIME_FORMAT) - datetime.strptime(WAKEUP_TIME_BEFORE_SUNRISE, TIME_FORMAT)
  wakeup_time = str(wakeup_time)[:-3]
  prayer_times_list[0] = wakeup_time
  return prayer_times_list

def get_prayer_times(city_name):
  url = f"https://dailyprayer.abdulrcs.repl.co/api/{city_name}"
  response = requests.get(url)
  data = response.json()
  #print(data['city'])
  #print(data['date'])
  prayer_time_list = []
  print("==Prayer Times==")
  for prayer in data["today"]:
    prayer_time_list.append(data["today"][prayer])
    print(prayer + ": " + data["today"][prayer])
  prayer_time_list = prayer_time_list[1:] # removing Fajar start time
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
  number_of_retries = 5  
  while True:
    retry_count = 1
    while(retry_count <= number_of_retries):    
        try:
            prayer_times_list = get_prayer_times("ingolstadt")
        except:
            retry_count = retry_count + 1
            print("RE-Trying to get prayer times")
            time.sleep(10)
            continue
        break
    current_time = get_current_time()
    prayer_times_list = replace_sunrise_with_wakeup_time(prayer_times_list, WAKEUP_TIME_BEFORE_SUNRISE)
    prayer_time_diff = get_prayer_time_diff(prayer_times_list, current_time)
    for pr_time in prayer_time_diff:
      if re.match(REGEX_MATCH, pr_time):
        print("_______prayer_________")
        adan = AudioSegment.from_wav("adan.wav")
        play(adan)
      else:
        print(pr_time)
    time.sleep(60)



if __name__ == "__main__":
  main()