# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 18:59:20 2022

@author: Mathieu Duteil

Imports and process data related to Space X launches from the SpaceX REST API
"""

import requests
import pandas as pd
import numpy as np
import datetime
 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def getBoosterVersion(data):
    """Takes the dataset and uses the rocket column to call the API and append 
    the data to the list"""
    for x in data['rocket']:
       if x:
        response = requests.get("https://api.spacexdata.com/v4/rockets/"+str(x)).json()
        BoosterVersion.append(response['name'])

def getLaunchSite(data):
    """ Takes the dataset and uses the launchpad column to call the API and 
    append the data to the list"""
    for x in data['launchpad']:
       if x:
         response = requests.get("https://api.spacexdata.com/v4/launchpads/"+str(x)).json()
         Longitude.append(response['longitude'])
         Latitude.append(response['latitude'])
         LaunchSite.append(response['name'])
         
def getPayloadData(data):
    """Takes the dataset and uses the payloads column to call the API and 
    append the data to the lists"""
    for load in data['payloads']:
       if load:
        response = requests.get("https://api.spacexdata.com/v4/payloads/"+load).json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])

def getCoreData(data):
    """Takes the dataset and uses the cores column to call the API and append 
    the data to the lists"""
    for core in data['cores']:
            if core['core'] != None:
                response = requests.get("https://api.spacexdata.com/v4/cores/"+core['core']).json()
                Block.append(response['block'])
                ReusedCount.append(response['reuse_count'])
                Serial.append(response['serial'])
            else:
                Block.append(None)
                ReusedCount.append(None)
                Serial.append(None)
            Outcome.append(str(core['landing_success'])+' '+str(core['landing_type']))
            Flights.append(core['flight'])
            GridFins.append(core['gridfins'])
            Reused.append(core['reused'])
            Legs.append(core['legs'])
            LandingPad.append(core['landpad'])


#Data extraction:
spacex_url="https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)

static_json_url='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
print(response.status_code)

data = pd.json_normalize(response.json())

# Selecting the features, the flight number, and date_utc:
data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

# Removing rows with multiple cores (those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket).
data = data[data['cores'].map(len)==1]
data = data[data['payloads'].map(len)==1]

# Since payloads and cores are lists of size 1 we also extract the single value in the list and replace the feature.
data['cores'] = data['cores'].map(lambda x : x[0])
data['payloads'] = data['payloads'].map(lambda x : x[0])

# Converting the date_utc to a datetime datatype, and then extracting the date leaving the time
data['date'] = pd.to_datetime(data['date_utc']).dt.date

# Restricting the dates of the launches
data = data[data['date'] <= datetime.date(2020, 11, 13)]


#Global variables 
BoosterVersion = []
PayloadMass = []
Orbit = []
LaunchSite = []
Outcome = []
Flights = []
GridFins = []
Reused = []
Legs = []
LandingPad = []
Block = []
ReusedCount = []
Serial = []
Longitude = []
Latitude = []

getBoosterVersion(data)
getLaunchSite(data)
getPayloadData(data)
getCoreData(data)

launch_dict = {'FlightNumber': list(data['flight_number']),
'Date': list(data['date']),
'BoosterVersion':BoosterVersion,
'PayloadMass':PayloadMass,
'Orbit':Orbit,
'LaunchSite':LaunchSite,
'Outcome':Outcome,
'Flights':Flights,
'GridFins':GridFins,
'Reused':Reused,
'Legs':Legs,
'LandingPad':LandingPad,
'Block':Block,
'ReusedCount':ReusedCount,
'Serial':Serial,
'Longitude': Longitude,
'Latitude': Latitude}

data_falcon = pd.DataFrame.from_dict(launch_dict)
data_falcon9 = data_falcon[data_falcon.BoosterVersion != 'Falcon 1']
data_falcon9.loc[:,'FlightNumber'] = list(range(1, data_falcon9.shape[0]+1))

# Replacing NaN values in PayloadMass with its mean value
data_falcon9['PayloadMass'] = data_falcon9['PayloadMass'].replace(np.nan, data_falcon9['PayloadMass'].mean())

# Saving the data set
data_falcon9.to_csv('dataset_part_1.csv', index=False)