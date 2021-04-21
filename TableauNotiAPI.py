# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:52:56 2021

@author: methee.s
"""
import requests

# Get ViewId of specific dashboard from Tableau Server
def GetViewId(dashboard):
    #Prepare for authentication
    server = '------Tableau Server URL------'
    urlHis = server + "auth/signin"
    headers = {"Content-Type": "application/json",
               "Accept":"application/json"}
    payload = { "credentials": {
                        		"personalAccessTokenName": "------Personal Access Token Name------",
                        		"personalAccessTokenSecret": "----------Personal Access Token----------",
                        		"site": {
                        			"contentUrl": "----content url----"
                        		}
                }
        }
    #Authenticate with Tableau Server
    res = requests.post(urlHis, headers=headers, json = payload)
    response =  res.json()
    token = response['credentials']['token']
    site_id = response['credentials']['site']['id']
    
    #Prepare to Get Dashboard(View) ID
    url = server + '/sites/'+site_id+'/views?filter=viewUrlName:eq:' + dashboard
    headers = {"Content-Type": "application/json",
               "Accept":"application/json",
               "X-Tableau-Auth": token}
    res = requests.get(url, headers=headers, json = {})
    response =  res.json()
    if len(response['views']) == 0 :
        print('No View Found!')
        return '','','',''
    elif len(response['views']['view']) > 1 :
        print('Multiple View Found')
        return response['views']['view'][0]['id'],site_id,headers,server
    else :
        print('View Found')
        return response['views']['view'][0]['id'],site_id,headers,server

#Get Image of dashboard based on view Name and send through LINE Notify
def GetImage(dashboard,filterName,filterValue,LineToken,message):
    view_id,site_id,headers,server = GetViewId(dashboard)
    print(view_id)
    if view_id != '':
        url = server +  '/sites/'+site_id+'/views/'+view_id+'/image' + '?vf_'+filterName+'='+filterValue
        res = requests.get(url, headers=headers, json = {})
        print('Got Image')
        #Send to LINE Notify
        LineUrl = 'https://notify-api.line.me/api/notify'
        LineHeaders = {'Authorization':'Bearer '+ LineToken}
        payload = {'message':message}
        file = {'imageFile':res.content}
        resp = requests.post(LineUrl, headers=LineHeaders , data = payload , files = file)
        print(resp)

