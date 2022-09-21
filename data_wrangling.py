# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 22:20:01 2022

@author: Mathieu Duteil

A program to explore the data of the problem 
and create a binary outcome variable.
"""

import pandas as pd

df=pd.read_csv("dataset_part_1.csv")
df.isnull().sum()/df.count()*100
df.dtypes
df['LaunchSite'].value_counts()
df['Orbit'].value_counts()
landing_outcomes = df['Outcome'].value_counts()
for i,outcome in enumerate(landing_outcomes.keys()):
    print(i,outcome)
bad_outcomes=set(landing_outcomes.keys()[[1,3,5,6,7]])
landing_class = []
for index, row in df.iterrows():
    if row['Outcome'] in bad_outcomes:
        landing_class.append(0)
    else:
        landing_class.append(1)
df['Class'] = landing_class
df.to_csv("dataset_part_2.csv", index=False)