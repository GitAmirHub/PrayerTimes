#Script to check prayer times by location using the aladhan API.

import requests
import datetime

#JSON get request to the API and record response
url = 'http://api.aladhan.com/v1/timingsByAddress'
params = dict(address = 'Regents Park Mosque, London, UK')
resp = requests.get(url, params)
data = resp.json()

#Get prayer times from the response and store individually
fajr_time = data['data']['timings']['Fajr']
sunrise_time = data['data']['timings']['Sunrise']
zuhr_time = data['data']['timings']['Dhuhr']
asr_time = data['data']['timings']['Asr']
sunset_time = data['data']['timings']['Sunset']
maghrib_time = data['data']['timings']['Maghrib']
isha_time = data['data']['timings']['Isha']

#Put prayer times into a dictionairy for easy access
prayer_times_today = {
    'Fajr' : fajr_time,
    'Sunrise' : sunrise_time,
    'Zuhr' : zuhr_time,
    'Asr' : asr_time,
    'Maghrib' : maghrib_time,
    'Sunset' : sunset_time,
    'Isha' : isha_time
}

#Print to console the prayer times
print(prayer_times_today)
