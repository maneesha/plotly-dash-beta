from dash import html, register_page, dcc 

register_page(__name__, path='/')

layout = html.Div([
    html.Br(),
    html.H2("About The Carpentries"),
    html.Div('Here is general information about the Carpentries.  The Carpentries teaches foundational coding and data science skills to researchers worldwide.'),
    dcc.Link('Read more', href='https://carpentries.org/about/'),
])