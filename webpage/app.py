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
                # About This Webpage 
                
                Hi, and welcome to our website made for our final project in the course [02806 Social Data Science and Visualization!](https://kurser.dtu.dk/course/02806)  
                
                Our project explores vehicle collisions in New York City using a [data set](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95) provided by the New York Police Department (NYPD).
                
                ## Defining Serious Collisions

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
        
                
                #Where Do Serious Collisions Occur? 
                
                '''),
                dcc.Graph(className="plotly", figure=figs.where_borough),
                dcc.Markdown('''
                             From the two plots above, we can see that Brooklyn has the highest number of collisions as well as the highest risk of a collision being serious. Most of inner Brooklyn has speed limits of 25 mph, while Belt Pwky that runs along the outskirts of Brooklyn has 50 mph. All in all, Brooklyn has a lot of roads with Belt Pkwy being a very has a lot of traffic to and from JFK airport. 

On the other end, we can see that while Manhattan has the lowest risk of a collision being serious, which matches well with Manhattan having very low speed limits. Now, instead of grouping by borough, let's see if any new patterns arise if we group on ZIP code instead!
                            '''),
                dcc.Graph(className="plotly", figure=figs.where_zip),
 
                dcc.Markdown("""
                    Here, we can see that while the probability of a collision being serious is higher on Manhattan, it is actually somewhat local! Some of the central ZIP codes in Brooklyn are definitely worth looking at. 
                    
                    ## When do crashes happen?"""),
                dcc.Graph(className="plotly", figure=figs.when_hour),
                dcc.Markdown("""
                    
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
            dcc.Graph(className="plotly", figure=figs.when_year)
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