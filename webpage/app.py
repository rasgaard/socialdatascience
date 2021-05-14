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

                For this project, we defined serious collisions as collisions where people are either injured or killed. By using this definition, the goal of [Vision Zero](https://en.wikipedia.org/wiki/Vision_Zero_(New_York_City)) is to eliminate all serious traffic collisions in New York City by 2024, and the analysis presented here could therefore help achieve this goal. For a future project, it would be interesting to look more into lethal car collisions, but there is *luckily* not a lot of data on that.  
                
                
                **Percentages:**
                
                | Number of persons injured  <br/> Number of persons killed | False  | True   |
                |---------------------------------------------------------|--------|--------|
                | False                                                   | 79.824 | 20.058 |
                | True                                                    | 0.087  | 0.028  |
                
                **Numbers**
                
                | Number of persons injured  <br/> Number of persons killed | False   | True   |
                |---------------------------------------------------------|---------|--------|
                | False                                                   | 1157463 | 290857 |
                | True                                                    | 1276    | 417    |

                As we can see from the tables above, very few collisions are deadly and therefore we defined *serious* as either injuring or deadly. 
        
                
                # Where Do Serious Collisions Occur? 
                
                '''),
                dcc.Graph(className="plotly", figure=figs.where_borough),
                dcc.Markdown('''
                From the two plots above, we can see that Brooklyn has the highest number of collisions as well as the highest risk of a collision being serious. Most of inner Brooklyn has speed limits of 25 mph, while Belt Pwky that runs along the outskirts of Brooklyn has 50 mph. All in all, Brooklyn has a lot of roads with Belt Pkwy being a very has a lot of traffic to and from JFK airport. 
                
                On the other end, we can see that while Manhattan has the lowest risk of a collision being serious, which matches well with Manhattan having very low speed limits. Now, instead of grouping by borough, let's see if any new patterns arise if we group on ZIP code instead!
                            '''),
                dcc.Graph(className="plotly", figure=figs.where_zip),
 
                dcc.Markdown("""
                Here, we can see that while the probability of a collision being serious is higher in Brooklyn, it is actually somewhat local! Some of the central ZIP codes in Brooklyn are definitely worth looking at. 
                
                # When Do Serious Collisions Occur?
                
                In the figure below, you can take a look at the serious collisions for all ZIP codes across time! Remember to hover over and check the data about that specific ZIP code at that specific time. 
                
                <sup> <sup> Also, some ZIP codes had very few observations for specific hours, so if you notice that some ZIP codes are disappearing and appearing, it is because ZIP codes with less than 10 total collisions for a given hour is removed. Check e.g ZIP 11697 at hours **09:00** versus **10:00**, it's right there at the bottom! <sup> <sup>
                """),
                dcc.Graph(className="plotly", figure=figs.when_hour),
                dcc.Markdown("""
                    In the figure above, we can see that generally, collisions have a high risk of being serious during the night and peaks around 04:00. We can also see that generally, there is a low risk of a collision being serious during rush hour in the morning (08:00 - 09:00). 
                    
                    # What Factors Make a Collision Serious? 
                    
                    In the figure below, you can investigate what factors make a collision serious! Which contributing factors make a collision serious? What is the most and least common contributing factor? These are questions that the figure below should be able to answer!
                    """),
                dcc.Graph(className='plotly', figure=figs.factor_scatter),
                dcc.Markdown("""
                    In the plot above, we can see that contributing factors that involve pedestrians/cyclists etc. are very dangerous, as we would expect. On the other hand, we can see that normal/slow-speed car-car collisions with contributing factors such as **Unsafe Lane Changing** and **Backing Unsafely** generally have a low risk of being lethal while high-speed, drug fueled collisions have a higher risk of being serious and ultimately lethal.
                    
                    Now we'll dive a bit deeper into a few selected topics of interest. Namely the effect of COVID-19 and see if we can spot interesting patterns in cases caused by distracted driving and alcohol involvement respectively.
                    """)
                    ], className='wrapper'),
        html.Div(children=[
        dcc.Tabs([
        dcc.Tab(label='Alcohol Involvement', children=[
            dcc.Markdown('''
            # Tab 2
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', className='tab-content'),

        ]),
        
        dcc.Tab(label='Driver Inattention/Distraction', children=[
            dcc.Markdown('''
            # Tab 3
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', className='tab-content'),

        ]),
        dcc.Tab(label='COVID-19', children=[
            dcc.Markdown('''
            # How has COVID-19 affected the probability of a collision being serious?
            
            Let's try to plot the probability of a collision being serious in a given day from January 2019 till December 2020.
            ''', className='wrapper'),

            dcc.Graph(className="wrapper", figure=figs.corona_probtime),

            dcc.Markdown("""
                The dots marks the government response to the spread of COVID-19. What we see here is an **increase** in risk when being involved in a collision after COVID-19 was first spotted in New York. How can that be? We suspect that it might be because of road inactivity due to everyone being encouraged to stay at home all of the sudden.
            """, className="wrapper"),
            
            dcc.Graph(className="wrapper", figure=figs.corona_count),

            dcc.Markdown("""
                Here we try to plot the number of non-serious collisions along with the number of serious collisions. As we suspected the rather high probability of a collision being serious isn't because more reckless driving is taking place, but rather less driving altogehter, resulting in less non-serious collisions.
            """, className="wrapper")
            ]),
        ]), html.Hr()], style={'width': '1420px', 'margin': '0 auto'}),
        
        html.Div(
            children=[
            
            dcc.Markdown('''
            # Summary 
            
            Here is where we write the conclusions about the data.
            '''),
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)