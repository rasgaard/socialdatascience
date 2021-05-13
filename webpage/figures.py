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

where_borough = make_subplots(rows=1, cols=2, 
                      specs=[[{'type': 'xy'},{"type": "mapbox"}]],
                      subplot_titles=('Bar chart of percentage of serious collisions', 
                                      'Choropleth of percentage of serious collisions'))

borough_pct = pd.DataFrame({'Borough' : [x.title() for x in df.groupby('BOROUGH').size().index], 
                       'Percentage' : (df_serious.groupby('BOROUGH').size().values / df.groupby('BOROUGH').size().values)}).sort_values(by='Percentage')

where_borough.add_trace(
    go.Bar(x = borough_pct['Borough'], y=borough_pct['Percentage']),
    row=1, col=1
)

where_borough.add_trace(
    go.Choroplethmapbox(geojson=boroughs, 
                        locations=borough_pct['Borough'], 
                        z=borough_pct['Percentage'], 
                        featureidkey='properties.BoroName'),
    row=1, col=2
)

where_borough.update_layout(mapbox_style="carto-positron", 
                    mapbox_center = {"lat": 40.730610, 
                                     "lon": -73.935242}, 
                    mapbox_zoom=9)

where_borough.update_layout(height=600, 
                    title_text='Ratio of serious collisions across Boroughs in New York City, 2012-2021')

where_borough['layout']['xaxis']['title']='Borough'
where_borough['layout']['yaxis']['title']=''

where_borough.update_layout(margin={"r":0,"t":75,"l":0,"b":0}, paper_bgcolor='#F7F7F7')



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