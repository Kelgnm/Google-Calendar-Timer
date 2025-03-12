import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# all the things to import for making custom google calendars

SCOPES  = ['https://www.googleapis.com/auth/calendar']  # getting the api from google and if modifying deleting token.json

def get_credentials(): # creating the credential command from credentials.json

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES) # token.json is a file that stores the users access and refresh tokens. 

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token: # if credentials are expired, refresh it
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # saves the credentials for the next run
        with open('token.json', 'w') as token: 
            token.write(creds.to_json()) 
        # Its being created automatically when the authorization flow completes for the first time

    # sends a value back to the part of the program that called the function
    return creds

def events(creds): # everything that its being in google calendars
    try:
        service = build("calendar", "v3", credentials=creds)

        event = { # a test manually created how its being created.
            'summary': 'THIS IS A TEST',
            'location': 'Online',
            'description': 'I CANT TAKE THIS ANYMORE',
            'start': {
                'dateTime': '2025-03-10T12:00:00',
                'timeZone': 'Europe/Sofia',
            },
            'end': {
                'dateTime': '2025-03-12T10:00:00',
                'timeZone': 'Europe/Sofia',
            },
        } # TO DO: make it automatic in real time

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event has been created! {event_result.get('htmlLink')}")

    # shows an error of the google calendar API
    except HttpError as error:
        print(f"An error has occured: {error}")

# compiling the entire code in one function
def main():
    creds = get_credentials()
    events(creds)

# exporting the function in the terminal
if __name__ == "__main__":
    main()