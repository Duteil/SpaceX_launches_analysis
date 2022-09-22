# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 02:12:46 2022

@author: Mathieu Duteil

This program creates a dashboard with plotly to gain insights on the data.
"""

import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_csv_file = 'spacex_launch_dash.csv'
spacex_df=pd.read_csv(spacex_csv_file)

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = list(set(spacex_df['Launch Site'].values))

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
                children=[html.H1('SpaceX Launch Records Dashboard',
                                  style={'textAlign': 'center', 
                                         'color': '#503D36',
                                         'font-size': 40}),
                          # TASK 1: Add a dropdown list to enable Launch Site selection
                          # The default select value is for ALL sites
                          dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': launch_sites[0], 'value': launch_sites[0]},
                                                    {'label': launch_sites[1], 'value': launch_sites[1]},
                                                    {'label': launch_sites[2], 'value': launch_sites[2]},
                                                    {'label': launch_sites[3], 'value': launch_sites[3]},
                                                     ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                            ),
                          html.Br(),

                          # TASK 2: Add a pie chart to show the total successful launches count for all sites
                          # If a specific launch site was selected, show the Success vs. Failed counts for the site
                          html.Div(dcc.Graph(id='success-pie-chart')),
                          html.Br(),

                          html.P("Payload range (Kg):"),
                          # TASK 3: Add a slider to select payload range
                          dcc.RangeSlider(id='payload-slider',
                                          min=0, max=10000, step=1000,
                                          marks={0: '0', 100: '100'},
                                          value=[min_payload, max_payload]),

                          # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                          html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                         ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
# Add computation to callback function and return graph
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby(['Launch Site'], as_index=False).mean()
        fig = px.pie(filtered_df, values='class', 
                    names='Launch Site', 
                    title='Launch Success Rate For All Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df['outcome'] = filtered_df['class'].apply(lambda x: 'Success' if (x == 1) else 'Failure')
        filtered_df['counts'] = 1
        fig = px.pie(filtered_df, values='counts', 
                     names='outcome', 
                     title='Launch Success Rate For ' + entered_site)        
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slider):
    filtered_df = spacex_df[
                            (slider[0] <= spacex_df['Payload Mass (kg)']) 
                            & (spacex_df['Payload Mass (kg)'] <= slider[1])
                           ]
    if entered_site == 'ALL':
        fig = px.scatter (filtered_df,
                          x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title='Launch Success Rate For All Sites')
        return fig
    else:
        # return the outcomes in pie chart for a selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        filtered_df['outcome'] = filtered_df['class'].apply(lambda x: 'Success' if (x == 1) else 'Failure')
        filtered_df['counts'] = 1
        fig = px.scatter (filtered_df,
                          x='Payload Mass (kg)', y='class',
                          color='Booster Version Category',
                          title='Launch Success Rate For ' + entered_site)
        return fig 
    
# Run the app
if __name__ == '__main__':
    app.run_server()