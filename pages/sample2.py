import dash
from dash import dcc, html, Input, Output, register_page 
import plotly.express as px
import pandas as pd

# Initialize page 
register_page(__name__, title="Sample2")

# Sample DataFrame (replace with your actual data)
df = pd.DataFrame({
    'country': ['USA', 'USA', 'CAN', 'CAN', 'MEX', 'MEX'],
    'year': [2020, 2021, 2020, 2021, 2020, 2021],
    'count_workshops': [10, 15, 7, 8, 5, 6]
})

# Get list of years for the slider
years = sorted(df['year'].unique())

layout = html.Div([
    html.H3("Workshops by Country"),
    dcc.Slider(
        id='year-slider',
        min=years[0],
        max=years[-1],
        step=1,
        value=years[0],
        marks={str(year): str(year) for year in years},
    ),
    dcc.Graph(id='bar-chart')
])

@dash.callback(
    Output('bar-chart', 'figure'),
    Input('year-slider', 'value')
)
def update_bar_chart(selected_year):
    filtered_df = df[df['year'] == selected_year]
    fig = px.bar(
        filtered_df,
        x='country',
        y='count_workshops',
        labels={'count_workshops': 'Workshop Count'},
        title=f'Workshops by Country in {selected_year}'
    )
    return fig