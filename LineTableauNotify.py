# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 21:06:03 2020

@author: methee.s
"""

from __future__ import print_function
import pickle
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import TableauNotiAPI as tbn


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '-----------ID of GOOGLE SHEET-----------'

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
try:
    with open('sheet-token.pickle', 'rb') as token:
        creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sheet-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('sheet-token.pickle', 'wb') as token:
            pickle.dump(creds, token)
except:
    print('Error Found')
    exit

service = build('sheets', 'v4', credentials=creds)

RANGE_NAME = 'Sheet1!A:F'

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
values = result.get('values', [])
#Convert to Pandas Dataframe
df = pd.DataFrame(values[1:], columns=values[0])
df.columns = ['DashboardName','Token','FilterName','FilterValue','Time','Message']

today = datetime.now()
theHour = today.hour
print(str(theHour))
for index, row in df.iterrows():
    if row['DashboardName'] != '' and str(row['Time']) == str(theHour):
        tbn.GetImage(row['DashboardName'],row['FilterName'],row['FilterValue'],row['Token'],row['Message'])
