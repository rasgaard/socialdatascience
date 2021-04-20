import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

data = pd.read_csv("avocado.csv")
data = data.query("type == 'conventional' and region == 'Albany'")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

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
                html.P(children="🥑", className="header-emoji"),
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
        dcc.Markdown('''
            # Introduction 
            
            This is the introduction, and here, we will show some general stuff about the dataset. 
            ''', style={'margin-left' : 50}),
        dcc.Tabs([
        dcc.Tab(label='Contributing Factor 1', children=[
            dcc.Markdown('''
            # Contributing Factor 1
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', style={'margin-left' : 50}),
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [15, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Contributing Factor 2', children=[
            dcc.Markdown('''
            # Contributing Factor 2
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', style={'margin-left' : 50}),
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [25, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Contributing Factor 3', children=[
            dcc.Markdown('''
            # Contributing Factor 3
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', style={'margin-left' : 50}),
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [5, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Contributing Factor 4', children=[
            dcc.Markdown('''
            # Contributing Factor 4
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', style={'margin-left' : 50}),
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [8, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Contributing Factor 5', children=[
            dcc.Markdown('''
            # Contributing Factor 5
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', style={'margin-left' : 50}),
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [11, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Contributing Factor 6', children=[
            dcc.Markdown('''
            # Contributing Factor 6
            
            This is just plain markdown. This can be used for writing some stuff.
            ''', style={'margin-left' : 50}),
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        ]),
        html.Div(
            children=[
            dcc.Markdown('''
            # Conclusions 
            
            Here is where we write the conclusions about the data.
            ''', style={'margin-left' : 50}),
            ],
            className="wrapper",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)