#Script to check prayer times by location using the aladhan API.

import requests
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Google Calendar API Stuff

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)


#JSON get request to the API and record response
url = 'http://api.aladhan.com/v1/timingsByAddress'
params = dict(address = 'Regents Park Mosque, London, UK')
resp = requests.get(url, params)
data = resp.json()

#Get prayer times from the response and store individually. Formatted with dattime strptime and strftime.
#Confusing currently but will refactor later.
fajr_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Fajr'], '%H:%M'), '%H:%M')
sunrise_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Sunrise'], '%H:%M'), '%H:%M')
zuhr_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Dhuhr'], '%H:%M'), '%H:%M')
asr_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Asr'], '%H:%M'), '%H:%M')
sunset_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Sunset'], '%H:%M'), '%H:%M')
maghrib_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Maghrib'], '%H:%M'), '%H:%M')
isha_time = datetime.datetime.strftime(datetime.datetime.strptime(data['data']['timings']['Isha'], '%H:%M'), '%H:%M')


#Put prayer times into a dictionairy for easy access.
#Jummah is a manual entry. Only changes when clocks go forward/back. 
prayer_times_today = {
    'Fajr' : fajr_time,
    'Sunrise' : sunrise_time,
    'Zuhr' : zuhr_time,
    'Asr' : asr_time,
    'Maghrib' : maghrib_time,
    'Sunset' : sunset_time,
    'Isha' : isha_time,
    'Jummah (Friday only)' : '13:00'
}

#Print to console the prayer times. Debug purposes. 
print(prayer_times_today)

#WHY DO I NEED TO DO SO MANY CONVERSIONS!!!!!
#THIS NEEDS TO BE DONE CLEANER!!!!!
timeobj_fajr = datetime.datetime.strptime(fajr_time, '%H:%M')
timeobj_sunrise = datetime.datetime.strptime(sunrise_time, '%H:%M')
timeobj_zuhr = datetime.datetime.strptime(zuhr_time, '%H:%M')
timeobj_asr = datetime.datetime.strptime(asr_time, '%H:%M')
timeobj_maghrib = datetime.datetime.strptime(maghrib_time, '%H:%M')
timeobj_sunset = datetime.datetime.strptime(sunset_time, '%H:%M')
timeobj_isha = datetime.datetime.strptime(isha_time, '%H:%M')

full_fajr_time = datetime.datetime.combine(datetime.date.today(), timeobj_fajr.time())
full_sunrise_time = datetime.datetime.combine(datetime.date.today(), timeobj_sunrise.time())
full_zuhr_time = datetime.datetime.combine(datetime.date.today(), timeobj_zuhr.time())
full_asr_time = datetime.datetime.combine(datetime.date.today(), timeobj_asr.time())
full_isha_time = datetime.datetime.combine(datetime.date.today(), timeobj_isha.time())
full_maghrib_time = datetime.datetime.combine(datetime.date.today(), timeobj_maghrib.time())
full_sunset_time = datetime.datetime.combine(datetime.date.today(), timeobj_sunset.time())

end_prayer_times = {
  'Fajr' : full_fajr_time + datetime.timedelta(0,0,0,0,5),
  'Sunrise' : full_sunrise_time + datetime.timedelta(0,0,0,0,5),
  'Zuhr' : full_zuhr_time + datetime.timedelta(0,0,0,0,5),
  'Asr' : full_asr_time + datetime.timedelta(0,0,0,0,5),
  'Maghrib' : full_maghrib_time + datetime.timedelta(0,0,0,0,5),
  'Sunset' : full_sunset_time + datetime.timedelta(0,0,0,0,5),
  'Isha' : full_isha_time + datetime.timedelta(0,0,0,0,5)
}

full_prayer_times = {
    'Fajr' : full_fajr_time,
    'Sunrise' : full_sunrise_time,
    'Zuhr' : full_zuhr_time,
    'Asr' : full_asr_time,
    'Maghrib' : full_maghrib_time,
    'Sunset' : full_sunset_time,
    'Isha' : full_isha_time
}


#Using Google Calendar API to add prayer times as an event and set reminder on event.
event = {
  'summary': 'Prayer time',
  'location': 'Home',
  'description': ' time',
  'start': {
    'dateTime': full_prayer_times['Fajr'],
    'timeZone': 'England/London',
  },
  'end': {
    'dateTime': end_prayer_times['Fajr'],
    'timeZone': 'England/London',
  },
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 1},
      {'method': 'popup', 'minutes': 1},
      ],
    },
  }

# for key in full_prayer_times:
#  event = {
#     'summary': key + 'Prayer time',
#     'location': 'Home',
#     'description': key + ' time',
#     'start': {
#       'dateTime': full_prayer_times[key],
#       'timeZone': 'England/London',
#     },
#     'end': {
#       'dateTime': end_prayer_times[key],
#       'timeZone': 'England/London',
#     },
#     'reminders': {
#       'useDefault': False,
#       'overrides': [
#         {'method': 'email', 'minutes': 1},
#         {'method': 'popup', 'minutes': 1},
#       ],
#     },
#   }
  
event = service.events().insert(calendarId='primary', body=event).execute()

print('Event created: %s' % (event.get('htmlLink')))
