# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 01:58:55 2022

@author: Mathieu Duteil

Analysis of the properties of the different launch sites with Folium
"""

import pandas as pd
import folium
import wget
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def draw_distance(site_map, color, lat1, long1, lat2, long2):
    coordinates = [[lat1,long1], [lat2,long2]]
    lines=folium.PolyLine(locations=coordinates, weight=1, color=color)
    site_map.add_child(lines)

# Downloading and read the `spacex_launch_geo.csv`
spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)

# Marking all launch sites on a map
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
marker = folium.map.Marker(
                            nasa_coordinate,
                            icon=DivIcon(
                                        icon_size=(20,20),
                                        icon_anchor=(0,0),
                                        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
                                        )
                            )
site_map.add_child(circle)
site_map.add_child(marker)


# Initialise the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=3)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
for idx in range(len(launch_sites_df)):
    site_coordinates = [launch_sites_df.at[idx,'Lat'],launch_sites_df.at[idx,'Long']]
    circle = folium.Circle(site_coordinates, radius=1000, color='#d35400', fill=True).add_child(folium.Popup(launch_sites_df.at[idx,'Launch Site']))
    marker = folium.map.Marker(
                            site_coordinates,
                            icon=DivIcon(
                                    icon_size=(20,20),
                                    icon_anchor=(0,0),
                                    html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % launch_sites_df.at[idx,'Launch Site'],
                                        )
                                )
    site_map.add_child(circle)
    site_map.add_child(marker)    


# Marking the success/failed launches for each site on the map:
marker_cluster = MarkerCluster()
spacex_df['marker_color'] = 'red'
spacex_df.loc[spacex_df['class'] == 1, 'marker_color'] = 'green'
site_map.add_child(marker_cluster)
for idx in range(len(spacex_df)):
    site_coordinates = [spacex_df.at[idx,'Lat'],spacex_df.at[idx,'Long']]
    marker = folium.map.Marker(
                            site_coordinates,
                            icon=DivIcon(
                                    icon_size=(20,20),
                                    icon_anchor=(0,0),
                                    html='<div style="font-size: 12; color:' + spacex_df.at[idx,'marker_color'] +'"><b>%s</b></div>' % spacex_df.at[idx,'Launch Site'],
                                        )
                                )
    marker_cluster.add_child(marker)
site_map


# Distances between a launch site and its proximities
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)
site_map.add_child(mouse_position)
site_map

# Distance to the coast:
coast = {'CCAFS LC-40':[28.56323, - 80.56786], 
         'CCAFS SLC-40':[28.56323, - 80.56786], 
         'KSC LC-39A':[28.58042, - 80.64222], 
         'VAFB SLC-4E':[34.63674, -120.62525]}
distance_coastline = []
for idx in range(len(launch_sites_df)):
    launch_site_lat = launch_sites_df.at[idx,'Lat']
    launch_site_lon = launch_sites_df.at[idx,'Long']
    coastline_lat = coast[launch_sites_df.at[idx,'Launch Site']][0]
    coastline_lon = coast[launch_sites_df.at[idx,'Launch Site']][1]
    distance_coastline.append(calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon))
    print(distance_coastline[idx])
    
water_color = 'blue'
for idx in range(len(launch_sites_df)):
    lat1 = coast[launch_sites_df.at[idx,'Launch Site']][0]
    long1 = coast[launch_sites_df.at[idx,'Launch Site']][1]
    lat2 = launch_sites_df.at[idx,'Lat']
    long2 = launch_sites_df.at[idx,'Long']
    draw_distance(site_map, water_color, lat1, long1, lat2, long2)
site_map


# Drawing the distance to the nearest railways, highways and cities:
close_railway = {'CCAFS LC-40':[28.57223, - 80.58542], 
                 'CCAFS SLC-40':[28.57223, - 80.58542], 
                 'KSC LC-39A':[28.57316, - 80.65395], 
                 'VAFB SLC-4E':[34.63635, -120.62375]}

close_highway = {'CCAFS LC-40':[28.56284, - 80.57074], 
                 'CCAFS SLC-40':[28.56284, - 80.57074], 
                 'KSC LC-39A':[28.57337, - 80.65569], 
                 'VAFB SLC-4E':[34.63893, -120.45806]}

close_city = {'CCAFS LC-40':[28.09879, - 80.64779], 
              'CCAFS SLC-40':[28.09879, - 80.64779], 
              'KSC LC-39A':[28.09879, - 80.64779], 
              'VAFB SLC-4E':[34.63288, -120.48542]}

landmark_color = {'railway': 'dimgray', 
                  'highway': 'sienna', 
                  'city': 'red'}

landmark_dict = {'railway': close_railway, 
                  'highway': close_highway, 
                  'city': close_city}

for landmark in ['railway', 'highway', 'city']:
    distance_landmark = []
    for idx in range(len(launch_sites_df)):
        lat1 = landmark_dict[landmark][launch_sites_df.at[idx,'Launch Site']][0]
        long1 = landmark_dict[landmark][launch_sites_df.at[idx,'Launch Site']][1]
        lat2 = launch_sites_df.at[idx,'Lat']
        long2 = launch_sites_df.at[idx,'Long']
        draw_distance(site_map, landmark_color[landmark], lat1, long1, lat2, long2)        

site_map    