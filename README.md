# tableau-linenotify
Python code to get dashboard/view image from Tableau server and send through LINE Notify

## Prerequisite
1. Python
2. Gmail account

## Preparation
- Enable G-Sheet API  in your google console  
  gsheet : [https://developers.google.com/sheets/api/quickstart/python]
- Copy "credential.json" from Google Console to location of python code
- Install require package
  ```
  google-api-python-client  
  google-auth-httplib2  
  google-auth-oauthlib
  ```
- Modify LineTableauNotify.py to include
  ```
  Sheet ID
  Sheet Range
  ```
- Get personal access token from your tableau server
  [https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm]
- Modify TableauNoti.py to include
  ```
  Personal Access Token (Name and Token)
  Tableau server URL 
  ```

## Running
  Run the code by call
  ```
  LineTableauNotify.py
  ```
