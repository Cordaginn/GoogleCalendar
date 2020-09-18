import icalendar
import requests
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json


def main():
    config = None
    with open("config.json","r") as conf:
        config = json.load(conf)
    tokenPATH = config["tokenPATH"]
    SCOPES = config["scopes"]
    credentialsPATH = config["credentialsPATH"]
    calendar_id = config["calendarId"]
    targetCalendarUrl = config["calendarURL"]
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenPATH):
        with open(tokenPATH, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsPATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenPATH, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for event in events['items']:
            service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    response = requests.get(targetCalendarUrl)
    google_calendar = icalendar.Calendar().from_ical(response.content)
    for component in google_calendar.walk():
        if component.name == "VEVENT":
            event_title = re.split(professors_name_reg, component.get('summary'))[0]
            event_professors = "\n".join(re.findall(professors_name_reg, component.get('summary')))
            event_start = bytes.decode(component.get('dtstart').to_ical(),'utf-8')
            event_end = bytes.decode(component.get('dtend').to_ical(),'utf-8')
            event_start = icalendar.vDatetime.from_ical(event_start).isoformat('T')
            event_end = icalendar.vDatetime.from_ical(event_end).isoformat('T')
            event = {
                'summary': event_title,
                'description':event_professors,
                'start':{
                  'dateTime':event_start,  
                } ,
                'end':{
                    'dateTime':event_end,
                },
                'reminders':{
                    'useDefault': False,
                    'overrides':[
                        {
                            'method':'popup',
                            'minutes': 60
                        },
                        {
                            'method':'popup',
                            'minutes': 120
                        }
                    ]
                }
            }
            service.events().insert(calendarId=calendar_id,body=event).execute()

if __name__ == '__main__':
    main()