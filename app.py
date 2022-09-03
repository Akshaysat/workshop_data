import pandas as pd
import requests
import json
import time
import os
import streamlit as st

def registered_data(workshop_id,offset = 1,df1 = 0):
    #print(offset)
    
    if offset == 1:
        url = "https://catalog.prod.learnapp.com/kraken/catalog/workshops/"+ workshop_id +"/registrations"
        df1 = pd.DataFrame(columns = ['email'])
        df1 = df1.set_index(['email'])
    else:
        url = "https://catalog.prod.learnapp.com/kraken/catalog/workshops/"+ workshop_id +"/registrations?offset=" + str(offset)

    payload={}
    headers = {
      'authority': 'catalog.prod.learnapp.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'authorization': token,
      'content-type': 'application/json',
      'if-none-match': 'W/"37e9-q1+5VenwgpUeLkX7K+6/dedhj7E"',
      'origin': 'https://kraken.learnapp.com',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
      'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)
    #df1 = df1.append(pd.DataFrame(pd.DataFrame(data['users'])[['email','phoneNumber']]), ignore_index = True)
    df1 = df1.append(pd.DataFrame(pd.DataFrame(data['users'])['phoneNumber']), ignore_index = True)
    
    try:
        offset = data['offset']
        df1 = registered_data(workshop_id,offset,df1)
    except:
        #print('done')
        df1.dropna(axis = 0,inplace = True)
        df1 = df1.set_index('phoneNumber')
            
    return df1

def get_workshop_id(workshop_canonical_title):
    print(token)
    url = "https://catalog.prod.learnapp.com/kraken/catalog/workshops/titles/" + workshop_canonical_title
    payload={}
    headers = {
      'authority': 'catalog.prod.learnapp.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'authorization': token,
      'content-type': 'application/json',
      'origin': 'https://kraken.learnapp.com',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
      'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data['id']

def workshop_details(workshop_canonical_title):
    
    workshop_id = get_workshop_id(workshop_canonical_title)
    df = registered_data(workshop_id)
    
    return df


st.title("Workshop Registered User's Data Tool")

global token
token = st.text_input('Authorization token:', help = "Open Network Logs")

workshop_canonical_title = st.text_input('Workshop Cananical Title:')

#df = workshop_details('how-to-capture-theta-decay-')

if st.button('Submit'):
    with st.spinner('Fetching data ... '):
        df = workshop_details(workshop_canonical_title)
        csv = df.to_csv().encode('utf-8')

        st.download_button(
        "Download CSV",
        csv,
        workshop_canonical_title + ".csv",
        "text/csv",
        key='download-csv',
        #help = ticker + ' data available to download'
        )