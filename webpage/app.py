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
                
                #Defining Serious Collisions

                For this project, we defined serious collisions as collisions where people are either injured or killed. By using this definition, the goal of Vision Zero is to eliminate all serious traffic collisions in New York City by 2024, and the analysis presented here could therefore help achieve this goal. For a future project, it would be interesting to look more into lethal car collisions, but there is *luckily* not a lot of data on that.  
                
                
                **Percentages:**
                
                | Number of persons injured <br> Number of persons killed | False  | True   |
                |---------------------------------------------------------|--------|--------|
                | False                                                   | 79.824 | 20.058 |
                | True                                                    | 0.087  | 0.028  |
                
                **Numbers**
                
                | Number of persons injured <br> Number of persons killed | False   | True   |
                |---------------------------------------------------------|---------|--------|
                | False                                                   | 1157463 | 290857 |
                | True                                                    | 1276    | 417    |

                As we can see from the tables above, very few collisions are deadly and therefore we defined *serious* as either injuring or deadly. 
                
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
                dcc.Graph(className='plotly', figure=figs.when_year),
                dcc.Markdown("""
                    By plotting the yearly risk of a collision being serious we notice that the year 2020 has a substantial in comparison to the rest of the years. As the whole world was affected by a pandemic most of this year we suspect that COVID-19 plays a significant role in the risk being this high. We'll investigate this further in the "COVID-19" tab below.
                            """)
                    ], className='wrapper'),
        html.Div(children=[
        dcc.Tabs([
        dcc.Tab(label='COVID-19', children=[
            dcc.Markdown('''
            # How has COVID-19 affected the probability of a collision being serious?
            
            As seen above, we notice an increase in risk in the year 2020. Let's try to "zoom in" on the plot to include the months from 2019 and 2020.
            ''', className='tab-content'),
            dcc.Graph(className="plotly", figure=figs.corona_probtime)
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
    app.run_server(debug=False)