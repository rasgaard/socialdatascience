import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from urllib.request import urlopen
import json

import pandas as pd
import numpy as np


df = pd.read_csv("preprocessed_collisions.csv")

df['YEAR'] = pd.to_datetime(df['CRASH DATE']).dt.year
df['MONTH'] = pd.to_datetime(df['CRASH DATE']).dt.month

df_serious = df.query("(`NUMBER OF PERSONS INJURED` + `NUMBER OF PERSONS KILLED`) > 0")


# WHERE BOROUGH PLOT
with urlopen('https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson') as response:
    boroughs = json.load(response)

total        = pd.DataFrame(df.groupby('BOROUGH').size().reset_index().values, columns=['Borough', 'Total count'])
only_injured = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] == 0)&(df['NUMBER OF PERSONS INJURED'] > 0)].groupby('BOROUGH').size().reset_index().values, columns=['Borough', 'Injured count'])
only_killed  = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] > 0)&(df['NUMBER OF PERSONS INJURED'] == 0)].groupby('BOROUGH').size().reset_index().values, columns=['Borough', 'Killed count'])
both         = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] > 0)&(df['NUMBER OF PERSONS INJURED'] > 0)].groupby('BOROUGH').size().reset_index().values, columns=['Borough', 'Injured and killed count'])

df_borough = pd.merge(pd.merge(pd.merge(total, only_injured, on='Borough'), only_killed, on='Borough'), both, on='Borough')

df_borough = df_borough[['Borough', 'Injured count', 'Killed count', 'Injured and killed count', 'Total count']]
df_borough['p'] = df_borough[['Injured count', 'Killed count', 'Injured and killed count']].sum(axis=1)/df_borough['Total count']
df_borough['Borough'] = df_borough['Borough'].str.title()

where_borough = make_subplots(rows=1, cols=2, specs=[[{'type': 'xy'},{"type": "mapbox"}]],
                   subplot_titles=('Total number of collisions', 'Probability of a collision being serious'))

where_borough.add_trace(
    go.Bar(x = df_borough['Borough'], y=df_borough['Total count'], customdata=df_borough[['Borough', 'Injured count', 'Killed count', 'Injured and killed count', 'Total count']]),
    row=1, col=1
)

where_borough.add_trace(
    go.Choroplethmapbox(geojson=boroughs, locations=df_borough['Borough'], z=df_borough['p'], featureidkey='properties.BoroName',
    customdata=df_borough[['Borough', 'Injured count', 'Killed count', 'Injured and killed count', 'Total count']],
    marker_opacity=0.5,  zmin=0, zmax=0.25, colorscale="Viridis"),
    row=1, col=2
)
#'style': "stamen-terrain"
#carto-positron
where_borough.update_layout(mapbox_style="carto-positron", mapbox_center = {"lat": 40.712772, "lon": -74.006058}, mapbox_zoom=9)
where_borough.update_layout(height=600, width=1200, title_text='Car collisions across Borough in New York City, 2012-2020')

#Update the bar trace.
where_borough.update_traces(
    hovertemplate="<br>".join([
        "<b>%{customdata[0]}</b>",
        "",
        "Number of collisions with only injured: %{customdata[1]}",
        "Number of collisions with only killed: %{customdata[2]}",
        "Number of collisions with both killed and injured: %{customdata[3]}",
        "",
        "Total number of collisions: %{y:.}",
    ]),
    marker_color='rgb(43,174,128)',
    selector=dict(type="bar")
)

where_borough.update_traces(
    hovertemplate="<br>".join([
        "<b>%{customdata[0]}</b>",
        "",
        "Number of collisions with only injured: %{customdata[1]}",
        "Number of collisions with only killed: %{customdata[2]}",
        "Number of collisions with both killed and injured: %{customdata[3]}",
        "Total number of collisions: %{customdata[4]:,}",
        "",
        "Probability of a collision being serious: %{z}",
    ]),
    selector=dict(type="choroplethmapbox")
)


where_borough.update_layout(xaxis={'categoryorder':'total descending'})
# edit axis labels
where_borough['layout']['xaxis']['title']='Borough'
where_borough['layout']['yaxis']['title']='Number of collisions'

# WHERE ZIP CODE PLOT
with urlopen('https://raw.githubusercontent.com/fedhere/PUI2015_EC/master/mam1612_EC/nyc-zip-code-tabulation-areas-polygons.geojson') as response:
    counties = json.load(response)

ZIP_pct = pd.DataFrame(df_serious['ZIP CODE'].value_counts() / df['ZIP CODE'].value_counts()).reset_index()
ZIP_pct.columns = ['ZIP CODE', 'Percentage']
ZIP_pct = ZIP_pct[~(ZIP_pct['Percentage'] > .99)]

where_zip = px.choropleth_mapbox(ZIP_pct, 
                                        geojson=counties, locations='ZIP CODE',
                                        color='Percentage', featureidkey="properties.postalCode",
                                        color_continuous_scale="Viridis",
                                        # range_color=(0, 1),
                                        center={"lat": 40.730610, "lon": -73.935242},
                                        labels={'values':'Number of crashes'},
                                        mapbox_style="carto-positron", zoom=9)

where_zip.update_geos(fitbounds="locations", visible=False)
where_zip.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#F7F7F7')


# HOURLY RISK PLOT
hourly_risk = pd.DataFrame(pd.to_datetime(df_serious['CRASH TIME']).dt.hour.value_counts() \
                       / pd.to_datetime(df['CRASH TIME']).dt.hour.value_counts()).reset_index()
hourly_risk.columns = ['Hour', 'Percentage']

when_hour = px.bar(hourly_risk,
                   x='Hour', y='Percentage')
when_hour.update_layout(xaxis={'tickmode':'linear', 
                               'title': 'Hour of the day'},
                       yaxis={'title': 'Risk of serious collision'},title="Hourly risk of a collision being serious",
                       paper_bgcolor='#F7F7F7')


# YEARLY RISK PLOT
yearly_risk = pd.DataFrame(df_serious['YEAR'].value_counts() \
                         / df['YEAR'].value_counts()).reset_index()
yearly_risk.columns = ['Year', 'Percentage']

when_year = px.bar(yearly_risk,
                   x='Year', 
                   y='Percentage')

when_year.update_layout(xaxis={'tickmode':'linear', 
                               'title': 'Year'},
                        yaxis={'title': 'Risk of serious collision'},
                        title="Yearly risk of a collision being serious",
                        paper_bgcolor='#F7F7F7')