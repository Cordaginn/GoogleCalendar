# GoogleCalendar
## Description 

This app gets your target calendar of format ***ics*** and parse them into your own google calendar 
 
## :no_entry_sign: WARNING! :no_entry_sign:

Just use *additional one calendar*,intended for *this app only*. To preventing losing your own events **YOU MUST** use calendar that not intended for your personal events.

### Config.json
You should to setup config file for this app.
Config patern:
```
{
    "calendarURL" : "http://urlToDownloadingICSfileOfYourTargetCalendar.com",
    "calendarId" : "Identifier of calendar in Google Calendar",
    "tokenPATH" : "/path/tofile/that/named/token.pickle",
    "scopes" : ["https://www.googleapis.com/auth/calendar"],
    "credentialsPATH" : "/path/to/yours/credentials.json"
}
```

### Google Calendar ID
For using this app you need to know an identifier of yours calendar in Google Calendar application.

So, just go to the settings of your prepared calendar in Google Calendar

![image](https://user-images.githubusercontent.com/30126869/93640735-bf53af80-fa03-11ea-8160-6784f3a1f1a5.png)

In first line of section **Integrate calendar** you have seen yours calendar id

![image](https://user-images.githubusercontent.com/30126869/93641135-72bca400-fa04-11ea-98b3-b3902223fc06.png)
