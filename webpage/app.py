import dash
import dash_core_components as dcc
import dash_html_components as html

import figures as figs


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Car Collisions in New York City!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="💥🚨🚗", className="header-emoji"),
                html.H1(
                    children="Car Collisions in New York City", className="header-title"
                ),
                html.P(
                    children="Final project for 02806 Social Data Analysis and Visualization.",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                dcc.Markdown('''
                # Introduction 
                
                Hi, and welcome to our website made for our final project in the course [02806](https://kurser.dtu.dk/course/02806) Social Data Science and Visualization! 
                
                Our project explores vehicle collisions in New York City using a [data set](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95) provided by the New York Police Department (NYPD). In particular, we would like to focus on and analyze the collisions that resulted in a serious outcome. We define a serious outcome as a collision where at least one person was either injured or killed. Of the 1,450,554 records of collisions in the data set 292,951 are serious as per our definition which is about 20%.

                
                The website is thus aimed at providing insight as to where and when it is most likely for a collision to be serious as well as look at what is most likely to contribute to a collision being serious.
                


                ## Where do the collisions occur?
                '''),
                dcc.Graph(className="plotly", figure=figs.where_borough),
                dcc.Markdown('''


                            '''),
                dcc.Graph(className="plotly", figure=figs.where_zip),
 
                dcc.Markdown("""
                    Comment on the plot above
                    
                    ## When do crashes happen?"""),
                dcc.Graph(className="plotly", figure=figs.when_hour),
                dcc.Markdown("""
                    Comment on the plot above
                    """),
                dcc.Graph(className='plotly', figure=figs.when_year)
                    ], className='wrapper'),
        html.Div(children=[
        dcc.Tabs([
        dcc.Tab(label='Tab 1', children=[
            dcc.Markdown('''
            # Tab 1
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', className='tab-content'),
        ]),
        
        dcc.Tab(label='Tab 2', children=[
            dcc.Markdown('''
            # Tab 2
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', className='tab-content'),

        ]),
        
        dcc.Tab(label='Tab 3', children=[
            dcc.Markdown('''
            # Tab 3
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', className='tab-content'),

        ]),
        ]), html.Hr()], style={'max-width': '1420px', 'margin': '0 auto'}),
        
        html.Div(
            children=[
            
            dcc.Markdown('''
            # Conclusions 
            
            Here is where we write the conclusions about the data.
            '''),
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)