#Script to check prayer times by location using the aladhan API.

import requests
import datetime
from __future__ import print_function
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

#Print to console the prayer times
print(prayer_times_today)
