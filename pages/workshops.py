import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

layout = html.Div([
    html.H1('These are our Workshops'),
    html.Div("Data, Library, and Software Carpentry workshops teach some skills."),
    html.Br(),
    html.Div(id='analytics-output'),

]) # close outer html.Div 