import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

layout = html.Div([
    html.H1('These are our Instructors'),
    html.Div("Some text about the instructors. They teach our workshops."),
    html.Br(),
    html.Div(id='analytics-output'),

]) # close outer html.Div 

