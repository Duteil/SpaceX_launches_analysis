# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 23:42:30 2022

@author: Mathieu Duteil

As none of the tools provided worked, I had to realise this exercise with 
Pandas rather than SQL, which would have been much simpler.
This code is meant to be used with the dataset provided on the Github, which
is formatted differently from the one provided by Coursera.
"""

import pandas as pd
import numpy as np

#%%
# Names of the unique launch sites in the space mission
spaceX_path = 'launch data.csv'
df = pd.read_csv(spaceX_path)
print("numbers by launch site: \n", df['Launch site'].value_counts())

#%%
# 5 records where launch sites begin with the string 'CCA'
i=0
j=0
while i<5:
    if df.at[j,'Launch site'][0:3] == 'CCA':
        i += 1
        print(df.iloc[j])
    j+=1

#%%
# Total payload mass carried by boosters launched by NASA (CRS)
NASA_df = df[df["Customer"] == "NASA"]
total_mass = sum(NASA_df['Payload mass'])
print("The total payload sent by SpaceX for NASA has been: " + str(total_mass) + " kg.")

#%%
# Average payload mass carried by booster version F9 v1.1
F9_11_df = df[df["Booster version"] == 'F9 v1.1']
mass_list = F9_11_df['Payload mass']
print("The average payload sent by SpaceX by rockets F9 v1.1 has been: " + str(np.mean(mass_list)) + " kg.")

#%%
# Date of the first succesful landing outcome in ground pad
i = 0
while df['Booster landing'][i] != 'Success (ground pad)':
    i+=1
print("The first successful ground landing was achieved on ", df["Date"][i])

#%%
# List the names of the boosters which have success in drone ship 
# and have payload mass greater than 4000 but less than 6000
drone_ship_success_df = df[df['Booster landing'] == 'Success (drone ship)']
success_booster = set()
for i in drone_ship_success_df.index:
    if drone_ship_success_df.at[i,"Payload mass"] > 4000 and drone_ship_success_df.at[i,"Payload mass"] < 6000:
        success_booster.add(drone_ship_success_df.at[i,'Booster version'])
print("The boosters that have succeeded in landing on a drone ship and proven capable of carrying payloads between 4 and 6 tons are: " + str(success_booster))

#%%
# Total number of successful and failure mission outcomes
print(str(df['Launch outcome'].value_counts()))

#%%
max_mass = max(df['Payload mass'])
max_mass_df = df[df['Payload mass'] == max_mass]
print("The versions of the booster that have carried the highest load are: ", set(max_mass_df['Booster version'].values))

#%%
# month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015
month_dict = {'01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
events_2015 = pd.DataFrame(columns = ['month', 'Landing outcome', 'Booster version', 'Launch site'])
for i in df.index:
    if df.at[i, "Date"][-4:] == '2015' and df.at[i,'Booster landing'] == 'Failure (drone ship)':
        month = month_dict[df.at[i,'Date'][3:5]]
        booster_version = df.at[i,'Booster version']
        launch_site = df.at[i,'Launch site']
        events_2015 = events_2015.append({'month':month, 'Landing outcome':'Failure (drone ship)', 'Booster version':booster_version, 'Launch site':launch_site}, ignore_index=True)
print(events_2015)

#%%
# successful landing outcomes between the date 04-06-2010 and 20-03-2017
future = True
for j in range(len(df.index)):
    idx = df.index[len(df.index)-j-1]
    if df.at[idx,'Date'][-7:] == '03-2017' and int(df.at[idx,'Date'][:2]) <= 20:
        future = False
    if not future and 'Success' in df.at[idx,'Booster landing']:
        print('A successful launch occured on ', df.at[idx,'Date'])