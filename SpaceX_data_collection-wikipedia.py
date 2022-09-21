# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:15:12 2022

@author: Mathieu Duteil

Collects Falcon 9 historical launch records from a Wikipedia page titled 
List of Falcon 9 and Falcon Heavy launches
"""

import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd

def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def date_conversion(date):
    month_dict = {'January':'01', 
                  'February':'02', 
                  'March':'03', 
                  'April':'04', 
                  'May':'05', 
                  'June':'06', 
                  'July':'07', 
                  'August':'08', 
                  'September':'09', 
                  'October':'10', 
                  'November':'11', 
                  'December':'12'}
    day, month, year = date.split()
    if len(day) == 1:
        day = '0' + day
    month = month_dict[month]
    date = day + '-' + month + '-' + year
    return date

def time_conversion(time):
    f = time.find(':')
    if f == 1:
        time = '0' + time
    time = time + ':00'
    return time

def format_site(tag):
    site = tag.text.strip()
    if 'Cape Canaveral' in site:
        site = site.replace('Cape Canaveral', 'CCAFS')
    site.replace(',',' ')
    f = site.find('[')
    if f!=-1:
        f0 = site.find(']')
        site = site[0:f] + site[f0+1:]
    return site

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell 
    Input: the  element of a table data cell extracts extra row
    """
    out=''.join([booster_version for i,booster_version in enumerate( table_cells.strings) if i%2==0][0:-1])
    return out

def landing_status(landing_cell):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    status = landing_cell.text.strip()
    f = status.find('[')
    while f !=-1:
        f0 = status.find(']')
        status = status[0:f] + status[f0+1:]
        f = status.find('[')
    f = status.find('(')
    if f != -1 and status[f-1]!=' ':
        status = status[:f] + ' ' + status[f:]
    status = status.strip()
    return status


def get_mass(mass_cell):
    mass=unicodedata.normalize("NFKD", mass_cell.text).strip()
    f=mass.find('–')
    mass=mass[0:f].strip()
    f=mass.find("kg")
    mass=mass[0:f].strip()
    if '~' in mass:
        mass = mass[1:]
    mass = ''.join(c for c in mass if c.isdigit())
    if not mass:
        mass=0
    return mass


def get_title_from_header(tag):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    column_name = str(tag)
    print(column_name)
    f = 0
    while f != -1:
        f0 = column_name.find('>')
        if column_name[f:f0+1] == '<br/>':
            column_name = column_name.replace('<br/>', ' ')
        else:
            column_name = column_name[0:f] + column_name[f0+1:]
        f = column_name.find('<')
    f = column_name.find('[')
    if f != -1:
        f0 = column_name.find(']')
        column_name = column_name[0:f] + column_name[f0+1:]
    column_name = column_name.strip()       
    print(column_name)
    
    # Filter the digit and empty names
    if not(column_name.strip().isdigit()):
        column_name = column_name.strip()
        return column_name
    else:
        print(column_name)


# We now extract data from the Wikipedia page on SpaceX launches:
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches"
# Uncomment to limit the data to up to June 9th 2021, as requested by the course:
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

column_names = []
response = requests.get(static_url)
soup_wiki = BeautifulSoup(response.text, 'html.parser')
html_tables = soup_wiki.find_all('table')
first_launch_table = html_tables[2]
for th in first_launch_table.find_all('th', scope="col"):
    name = get_title_from_header(th)
    if name is not None and len(name) > 0:
        column_names.append(name)

launch_dict= dict.fromkeys(column_names)

# Date and time is replaced with two separate columns, "Date" and "Time"
del launch_dict['Date and time (UTC)']
launch_dict['Date'] = None
launch_dict['Time (UTC)'] = None
launch_dict['Booster version'] = launch_dict['Version, Booster']
del launch_dict['Version, Booster']


# The existing columns of launch_dict are initialised as empty lists:
for key in launch_dict.keys():
    launch_dict[key] = []

extracted_row = 0
#Extract each table 
for table_number,table in enumerate(soup_wiki.find_all('table',"wikitable plainrowheaders collapsible")):
   # get table row 
    for rows in table.find_all("tr"):
        flag = True
        #check to see if first table heading is as number corresponding to launch a number 
        if rows.th and rows.th.string:
            flight_number=rows.th.text.strip()
            flag=flight_number.isdigit()
        else:
            flag=False
        #get table element 
        row=rows.find_all('td')
        #if it is a number, save cells in a dictonary 
        if flag:
            extracted_row += 1
            launch_dict['Flight No.'].append(extracted_row)
            if len(row)== 0:
                print(row)
            datatimelist=date_time(row[0])
            date = datatimelist[0].strip(',')
            date = date_conversion(date)
            launch_dict['Date'].append(date)
            time = datatimelist[1]
            time = time_conversion(time)
            launch_dict['Time (UTC)'].append(time)
            bv=booster_version(row[1])
            if not(bv):
                bv=row[1].a.string
            launch_dict['Booster version'].append(bv)
            launch_site = format_site(row[2])
            launch_dict['Launch site'].append(launch_site)
            payload = row[3].a.string
            launch_dict['Payload'].append(payload)
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            orbit = row[5].a.string
            launch_dict['Orbit'].append(orbit)
            if row[6].a is not None:
                customer = row[6].a.string
            else:
                customer = row[6]
            launch_dict['Customer'].append(customer)
            launch_outcome = list(row[7].strings)[0]
            if launch_outcome[-1:] == '\n':
                launch_outcome = launch_outcome[:-1]
            launch_dict['Launch outcome'].append(launch_outcome)
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)
           
df=pd.DataFrame(launch_dict)
spaceX_path = 'SpaceX.csv'
df.to_csv(spaceX_path, index=False)