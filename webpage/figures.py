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
df['DAY'] = pd.to_datetime(df['CRASH DATE']).dt.day
df['HOUR'] = pd.to_datetime(df['CRASH TIME']).dt.hour

df['CF_Drugs (illegal)'] = (df['CF_Drugs (illegal)']|df['CF_Drugs (Illegal)']); df.drop('CF_Drugs (Illegal)', axis=1, inplace=True)
df['CF_Cell Phone (hand-held)'] = (df['CF_Cell Phone (hand-held)']|df['CF_Cell Phone (hand-Held)']); df.drop('CF_Cell Phone (hand-Held)', axis=1, inplace=True)
df['CF_Illness'] = (df['CF_Illness']|df['CF_Illnes']); df.drop('CF_Illnes', axis=1, inplace=True)


df['YEARMONTH'] = df['YEAR'].astype(str)+'-'+df['MONTH'].astype(str)

df['YEARMONTHDAY'] = df['YEAR'].astype(str)+'-'+df['MONTH'].astype(str)+'-'+df['DAY'].astype(str)
df['YEARMONTHDAY'] = pd.to_datetime(df['YEARMONTHDAY'])

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
df_borough['p'] = (df_borough[['Injured count', 'Killed count', 'Injured and killed count']].sum(axis=1)/df_borough['Total count'])*100
df_borough['Borough'] = df_borough['Borough'].str.title()
df_borough['p_lethal'] = (df_borough[['Killed count','Injured and killed count']].sum(axis=1)/df_borough['Total count'])*100

where_borough = make_subplots(rows=1, cols=2, specs=[[{'type': 'xy'},{"type": "mapbox"}]],
                   subplot_titles=('Total number of collisions', 'Probability of a collision being serious'))

where_borough.add_trace(
    go.Bar(x = df_borough['Borough'], y=df_borough['Total count'], customdata=df_borough[['Borough', 'Injured count', 'Killed count', 'Injured and killed count', 'Total count']]),
    row=1, col=1
)

where_borough.add_trace(
    go.Choroplethmapbox(geojson=boroughs, locations=df_borough['Borough'], z=df_borough['p'], featureidkey='properties.BoroName',
    customdata=df_borough[['Borough', 'Injured count', 'Killed count', 'Injured and killed count', 'Total count', 'p_lethal']],
    marker_opacity=0.5,  zmin=0, zmax=25, colorscale="Viridis", colorbar={"title": '%'}),
    row=1, col=2
)
#'style': "stamen-terrain"
#carto-positron
where_borough.update_layout(mapbox_style="carto-positron", mapbox_center = {"lat": 40.712772, "lon": -74.006058}, mapbox_zoom=8.5)
where_borough.update_layout(height=600, title_text='Car collisions across Borough in New York City, 2012-2020')

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
        "Probability of a collision being serious: %{z}%",
        "Probability of a collision being lethal: %{customdata[5]:}%"
    ]),
    selector=dict(type="choroplethmapbox")
)

where_borough.update_layout(xaxis={'categoryorder':'total descending'}, margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor='#F7F7F7')
# edit axis labels
where_borough['layout']['xaxis']['title']='Borough'
where_borough['layout']['yaxis']['title']='Number of collisions'


# WHERE ZIP CODE PLOT
total        = pd.DataFrame(df.groupby(['BOROUGH', 'ZIP CODE']).size().reset_index().values, columns=['Borough', 'ZIP Code', 'Total count'])
only_injured = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] == 0)&(df['NUMBER OF PERSONS INJURED'] > 0)].groupby(['BOROUGH', 'ZIP CODE']).size().reset_index().values, columns=['Borough', 'ZIP Code', 'Injured count'])
only_killed  = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] > 0)&(df['NUMBER OF PERSONS INJURED'] == 0)].groupby(['BOROUGH', 'ZIP CODE']).size().reset_index().values, columns=['Borough', 'ZIP Code', 'Killed count'])
both         = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] > 0)&(df['NUMBER OF PERSONS INJURED'] > 0)].groupby(['BOROUGH', 'ZIP CODE']).size().reset_index().values, columns=['Borough', 'ZIP Code', 'Injured and killed count'])

df_zip_borough = pd.merge(pd.merge(pd.merge(total, only_injured, on=['Borough', 'ZIP Code'], how='left'), only_killed, on=['Borough', 'ZIP Code'], how='left'), both, on=['Borough', 'ZIP Code'], how='left')
df_zip_borough['Borough'] = df_zip_borough['Borough'].str.title()
df_zip_borough = df_zip_borough.fillna(0) #Fill missing values with 0.
df_zip_borough['p'] = df_zip_borough[['Injured count', 'Killed count', 'Injured and killed count']].sum(axis=1)/df_zip_borough['Total count']
df_zip_borough = df_zip_borough.loc[df_zip_borough['Total count'] > 100]

with urlopen('https://raw.githubusercontent.com/fedhere/PUI2015_EC/master/mam1612_EC/nyc-zip-code-tabulation-areas-polygons.geojson') as response:
    counties = json.load(response)
    
    
where_zip = px.choropleth_mapbox(df_zip_borough, 
                                        geojson=counties, locations='ZIP Code',
                                        color='p', featureidkey="properties.postalCode",
                                        custom_data=df_zip_borough[['Borough', 'ZIP Code', 'Total count', 'Injured count', 'Killed count', 'Injured and killed count']],
                                        color_continuous_scale="Viridis",
                                        range_color=(0, .4),
                                        center={"lat": 40.730610, "lon": -73.935242},
                                        labels={'values':'Number of crashes'},
                                        opacity=0.5,
                                        mapbox_style="carto-positron", zoom=9)

where_zip.update_traces(
    hovertemplate="<br>".join([
        "<b>%{customdata[1]}, %{customdata[0]}</b>",
        "",
        "Number of collisions with only injured: %{customdata[3]}",
        "Number of collisions with only killed: %{customdata[4]}",
        "Number of collisions with both killed and injured: %{customdata[5]}",
        "Total number of collisions: %{customdata[2]:}",
        "",
        "Probability of a collision being serious: %{z:}",
    ]),
    selector=dict(type="choroplethmapbox")
)

where_zip.update_geos(fitbounds="locations", visible=False)
where_zip.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='#F7F7F7')


# HOURLY RISK PLOT
total = pd.DataFrame(df.groupby(['BOROUGH','ZIP CODE','HOUR']).size().reset_index().values, columns=['BOROUGH', 'ZIP CODE', 'HOUR', 'N_TOTAL'])
injured = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] == 0)&(df['NUMBER OF PERSONS INJURED'] > 0)].groupby(['BOROUGH','ZIP CODE','HOUR']).size().reset_index().values, columns=['BOROUGH', 'ZIP CODE', 'HOUR', 'N_INJURED'])
killed = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] > 0)&(df['NUMBER OF PERSONS INJURED'] == 0)].groupby(['BOROUGH','ZIP CODE','HOUR']).size().reset_index().values, columns=['BOROUGH', 'ZIP CODE', 'HOUR', 'N_KILLED'])
both = pd.DataFrame(df.loc[(df['NUMBER OF PERSONS KILLED'] > 0)&(df['NUMBER OF PERSONS INJURED'] > 0)].groupby(['BOROUGH','ZIP CODE','HOUR']).size().reset_index().values, columns=['BOROUGH', 'ZIP CODE', 'HOUR', 'N_BOTH'])

df_when = pd.merge(pd.merge(pd.merge(total, injured, how='left', on = ['BOROUGH','ZIP CODE','HOUR']), killed, how='left', on=['BOROUGH','ZIP CODE','HOUR']), both, how='left', on=['BOROUGH','ZIP CODE','HOUR'])
df_when = df_when.fillna(0)

df_when = pd.merge(df_when, df.groupby(['BOROUGH','ZIP CODE','HOUR']).sum().reset_index()[['BOROUGH', 'ZIP CODE', 'HOUR'] + [x for x in df.columns if x.startswith('CF_')]], how='left', on=['BOROUGH', 'ZIP CODE', 'HOUR'])

subset = df_when[[x for x in df_when.columns if x.startswith('CF_') if x not in ['CF_nan', 'CF_Unspecified']]]

df_when = df_when.join(pd.DataFrame(subset.apply(lambda x: list(subset.columns[np.array(x).argsort()[::-1][:3]]), axis=1).to_list(),  columns=['Top1', 'Top2', 'Top3']))

df_when = df_when.drop([x for x in df_when.columns if x.startswith('CF_')], axis=1)

df_when['Top1'] = df_when['Top1'].str.replace('CF_','')
df_when['Top2'] = df_when['Top2'].str.replace('CF_','')
df_when['Top3'] = df_when['Top3'].str.replace('CF_','')

df_when['p'] = df_when[['N_INJURED', 'N_KILLED', 'N_BOTH']].sum(axis=1) / df_when['N_TOTAL']

df_when = df_when.loc[df_when['N_TOTAL'] > 10]

df_when.columns = ['Borough', 'ZIP code', 'Hour', 'Total number of collisions', 'Number of collisions with only injured', 'Number of collisions with killed', 'Number of collisions with both killed and injured', 'Most common contributing factor', '2nd most common contributing factor', '3rd most common contributing factor', 'Probability of a collision being serious']

when_hour = px.choropleth_mapbox(df_when, geojson=counties, locations='ZIP code', color='Probability of a collision being serious', 
                           hover_data = ['Total number of collisions', 'Number of collisions with only injured',
                                         'Number of collisions with killed',
                                         'Number of collisions with both killed and injured',
                                         'Most common contributing factor',
                                         '2nd most common contributing factor',
                                         '3rd most common contributing factor'],
                           featureidkey="properties.postalCode",
                           color_continuous_scale="Viridis",
                           range_color=(0, df_when['Probability of a collision being serious'].max()),
                           animation_frame="Hour",
                           category_orders={"Hour": list(np.append(np.arange(18,24), np.arange(0, 18)))},
                           center={"lat": 40.730610, "lon": -73.935242},
                           #labels={'values':'Number of crashes'},
                           mapbox_style="carto-positron", zoom=9, height = 800)

when_hour.update_layout(coloraxis_colorbar=dict(title="p",), margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor='#F7F7F7')


#FACTOR SCATTER PLOT
df_factor_scatter = pd.DataFrame()

for index_, df_ in df.groupby([df['NUMBER OF PERSONS KILLED']>0, df['NUMBER OF PERSONS INJURED'] > 0]):
    df_factor_scatter['Killed_' + str(index_[0]) + '_Injured_' + str(index_[1])] = df_[[x for x in df.columns if x.startswith('CF_')]].sum(axis=0).values
    
df_factor_scatter['Contributing Factor'] = [x.replace('CF_','') for x in df_[[x for x in df.columns if x.startswith('CF_')]].columns.tolist()]
df_factor_scatter.columns = ['No injured', 'Only injured', 'Only killed', 'Both injured and killed', 'Contributing factor']
df_factor_scatter = df_factor_scatter[['Contributing factor', 'No injured', 'Only injured', 'Only killed', 'Both injured and killed']]
df_factor_scatter['p_serious'] = df_factor_scatter.iloc[:,2:].sum(axis=1) / df_factor_scatter.iloc[:,1:].sum(axis=1)

df_factor_scatter['p_lethal'] = df_factor_scatter[['Only killed', 'Both injured and killed']].sum(axis=1)\
                    /df_factor_scatter[['No injured', 'Only injured', 'Only killed', 'Both injured and killed']].sum(axis=1)

df_factor_scatter = df_factor_scatter.loc[~df_factor_scatter['Contributing factor'].isin(['nan', 'Unspecified'])]

df_factor_scatter['p_serious'] = df_factor_scatter['p_serious']*100
df_factor_scatter['p_lethal']  = df_factor_scatter['p_lethal']*100

df_factor_scatter['Total collisions'] = df_factor_scatter[['No injured', 'Only injured', 'Only killed', 'Both injured and killed']].sum(axis=1)

factor_scatter = px.scatter(df_factor_scatter, x = 'Total collisions', y = 'p_serious', 
                            custom_data = ['Contributing factor', 'No injured', 'Only injured', 
                                           'Only killed', 'Both injured and killed','p_serious', 
                                           'p_lethal', 'Total collisions'], log_x=True, size = 'p_lethal', 
                                           title='Risk of being serious across factors. Size is the risk of collision being lethal.',
                                           height=900)
factor_scatter.update_layout(
    xaxis_title="Total number of collisions from 2013-2020",
    yaxis_title="Risk of collision being serious",
)

factor_scatter.update_traces(
    hovertemplate="<br>".join([
        "<b>%{customdata[0]}</b>",
        "",
        "Total number of collisions: %{customdata[7]}",
        "- Collisions with no killed or injured: %{customdata[1]}",
        "- Collisions with only injured %{customdata[2]}",
        "- Collisions with only killed %{customdata[3]}",
        "- Collisions with both killed and injured %{customdata[4]}",
        "",
        "Probability of a collision being serious: %{y:}%",
        "Probability of a collision being lethal : %{customdata[6]}%",
    ]),
    selector=dict(type="scatter"),
    marker_color='rgb(43,174,128)',
)

x_annot, y_annot = df_factor_scatter.loc[df_factor_scatter['Contributing factor'] == 'Glare'][['Total collisions', 'p_serious']].iloc[0]
factor_scatter.add_annotation(x = np.log10(x_annot), y = y_annot, text = "Glare is often serious, but not deadly<br>hence the small dot.", showarrow = True, yshift=0)

x_annot, y_annot = df_factor_scatter.loc[df_factor_scatter['Contributing factor'] == 'Driver Inattention/Distraction'][['Total collisions', 'p_serious']].iloc[0]
factor_scatter.add_annotation(x = np.log10(x_annot), y = y_annot, text = "Driver Inattention is the most <br> common contributing factor.", showarrow = True, yshift=0)

x_annot, y_annot = df_factor_scatter.loc[df_factor_scatter['Contributing factor'] == 'Alcohol Involvement'][['Total collisions', 'p_serious']].iloc[0]
factor_scatter.add_annotation(x = np.log10(x_annot), y = y_annot, text = "We will look at this later!", showarrow = True, yshift=0)

factor_scatter.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor='#F7F7F7')


recent_df = df.query("YEAR >= 2019")

corona_serious = recent_df.query("(`NUMBER OF PERSONS KILLED` + `NUMBER OF PERSONS INJURED`) > 0")
corona_nonserious = recent_df.query("(`NUMBER OF PERSONS KILLED` + `NUMBER OF PERSONS INJURED`) <= 0")

corona_prob = pd.DataFrame((corona_serious['YEARMONTHDAY'].value_counts() / recent_df['YEARMONTHDAY'].value_counts())).reset_index()
corona_prob.columns = ['TIME', 'PROB']
corona_prob['TIME'] = pd.to_datetime(corona_prob['TIME'])
corona_prob = corona_prob.sort_values(by='TIME')

actions = pd.DataFrame({"TIME": ["2020-03-7", "2020-03-9", "2020-03-10", "2020-03-12", "2020-03-12", "2020-03-15", "2020-03-16", "2020-03-20", "2020-03-25", "2020-03-27", "2020-03-28", "2020-04-6", "2020-04-9", "2020-04-15", "2020-04-16", "2020-05-1", "2020-05-7", "2020-05-14", "2020-05-15", "2020-05-15", "2020-05-23", "2020-06-8", "2020-06-15", "2020-06-22", "2020-07-10", "2020-07-16", "2020-08-7", "2020-08-19", "2020-10-1", "2020-10-1", "2020-10-6", "2020-11-12", "2020-11-25", "2020-12-8"],
                        "Action Taken": ["State of emergency declared.", "State began producing its own \nbrand of hand sanitizer.", "Governor Cuomo orders a coronavirus 'containment zone' in \nNew Rochelle, Westchester County, NY.", "All gatherings of less than 500 people ordered to cut capacity by 50%.\n All gatherings of more than 500 people ordered to cancel.", "All SUNY campuses ordered to close within a week, \nand then shift to online for the remainder of the semester.", "All New York City schools ordered \nto close until April 20.", "Cuomo coordinates with his counterparts in New Jersey and \nConnecticut to formulate uniform policies for shutdowns.", "State-wide stay-at-home order declared. \nAll non-essential businesses ordered to close\n. All non-essential gatherings canceled/postponed.", "Advisory issued ordering nursing homes to admit patients who\n test positive for the coronavirus and to not allow testing of prospective nursing home patients.\n This order was revoked on May 10.", "All schools statewide ordered to remain closed until April 15.", "All non-essential construction sites ordered to shut down.", "Statewide stay-at-home order and school\n closures extended to April 29.", "List of businesses deemed essential expanded.", "All state residents ordered to wear face masks/coverings\n in public places where social distancing is not possible.", "Statewide stay-at-home order and school closures extended to May 15.", "All schools and universities ordered to remain closed\n for the remainder of the academic year.", "Statewide four-phase reopening plan is first announced.", "Statewide state of emergency extended to June 13.", "Phase 1 of reopening allowed for counties that met qualifications. Five counties met qualifications and began reopening on this date.", "Drive-in theaters, landscaping/gardening businesses allowed to reopen state-wide (regardless of Phase 1 qualifications).", "Gatherings of up to ten people allowed as long as social distancing is practiced.", "New York City meets conditions for Phase 1, allowing the reopening of construction, manufacturing, agriculture, forestry, fishing, and select retail businesses that can offer curbside pickup.", "Four-phase reopening plan is modified to allow non-essential gatherings of 25 people upon entry of Phase 3, and 50 people upon entry of Phase 4.", "New York City meets conditions for Phase 2, allowing the reopening of outdoor dining at restaurants, hair salons and barber shops, offices, real estate firms, in-store retail, vehicle sales, retail rental, repair services, cleaning services, and commercial building management businesses.", "Malls allowed to open at 25% capacity for regions in Phase 4, with all patrons required to wear masks.", "New restrictions on bars/restaurants only allowing alcohol to be served only to people ordering food.", "Schools allowed to open in-person in the fall if certain conditions are met.", "Ban on ticketed music events at bars and restaurants.", "Exposure notification apps are added to notify users of potential exposure.", "The previous ban on ticketed events at bars and restaurants is ruled unconstitutional.", "Micro-cluster strategy is introduced, with the first micro-clusters being parts of Brooklyn and Queens.", "Bars, gyms, and any other business with a liquor license must close by 10 p.m. (restaurants as well, except for curbside pickup). \nHousehold gatherings limited to ten people.", "Previous restrictions on capacity through the micro-cluster strategy for places of worship is ruled unconstitutional.", "Hospital bed capacity statewide is demanded to be upgraded by 25 percent.",]})
actions['TIME'] = pd.to_datetime(actions['TIME'])
actions = pd.merge(actions, corona_prob)

corona_probtime = px.line(corona_prob, x='TIME', y="PROB")
corona_probtime.update_traces(line_color='rgb(43,174,128)')
corona_probtime.add_trace(go.Scatter(mode='markers',
                         x=actions['TIME'], 
                         y=actions['PROB'], 
                         text=actions['Action Taken'],
                         marker_color='#461969'))
corona_probtime.update_xaxes(rangeslider_visible=True, title="Time")
corona_probtime.update_layout(showlegend=False, 
                              yaxis={"title": "Probability of a collision being serious."}, 
                              margin={"r":0,"t":50,"l":0,"b":0}, 
                              paper_bgcolor='#F7F7F7')

corona_count = go.Figure()

corona_nonserious_count = corona_nonserious['YEARMONTH'].value_counts().rename_axis("Yearmonth").reset_index(name="counts")
corona_serious_count = corona_serious['YEARMONTH'].value_counts().rename_axis("Yearmonth").reset_index(name="counts")

corona_count.add_trace(go.Scatter(x=pd.to_datetime(corona_nonserious_count['Yearmonth']).sort_values(),
                         y=corona_nonserious_count['counts'],
                         mode="lines+markers",
                         name="Non-serious collisions",
                         marker_color='rgb(43,174,128)'))
corona_count.add_trace(go.Scatter(x=pd.to_datetime(corona_serious_count['Yearmonth']).sort_values(),
                         y=corona_serious_count['counts'],
                         mode="lines+markers",
                         name="Serious collisions",
                         marker_color='#461969'))
corona_count.update_layout(title="Comparing serious vs. non-serious collisions during COVID", margin={"r":0,"t":50,"l":0,"b":0}, paper_bgcolor='#F7F7F7')