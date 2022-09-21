# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 22:32:33 2022

@author: Mathieu Duteil

This program creates visualisation of the variables, 
so as to better understand their influence on the launch outcome.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("dataset_part_2.csv")
sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

# Relationship between Flight Number and Launch Site
sns.catplot(x='FlightNumber', y='LaunchSite', hue='Class', data=df)
plt.ylabel("Launch Site",fontsize=15)
plt.xlabel("Flight Number",fontsize=15)
plt.show()

# Relationship between Payload and Launch Site
sns.scatterplot(x='PayloadMass', y='LaunchSite', hue='Class', data=df)

# Relationship between success rate of each orbit type
orbit_df = df.groupby(['Orbit']).mean()
sns.barplot(data=orbit_df, x=orbit_df.index, y='Class')

# Relationship between FlightNumber and Orbit type
sns.scatterplot(x='FlightNumber', y='Orbit', hue='Class', data=df)

# Relationship between Payload and Orbit type
sns.scatterplot(x='PayloadMass', y='Orbit', hue='Class', data=df)

# Launch success yearly trend
year=[]
for i in df["Date"]:
    year.append(i.split("-")[0])
sns.lineplot(x=year, y=df['Class'])

# Creating dummy variables to categorical columns
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features_one_hot = pd.get_dummies(features, prefix=['Orbit ', 'LaunchSite ', 'LandingPad ', 'Serial '], columns=['Orbit', 'LaunchSite', 'LandingPad', 'Serial'])

# Casting all numeric columns to float64
features_one_hot.astype('float64')

features_one_hot.to_csv('dataset_part_3.csv', index=False)