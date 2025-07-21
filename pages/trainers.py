import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_url 
import os 
import pandas as pd 
import plotly.graph_objects as go


redash_api_key = os.getenv("REDASH_KEY_QUERY523")

redash_data_url = f"http://redash.carpentries.org/api/queries/523/results.json?api_key={redash_api_key}"

trainers_json = get_json_from_url(redash_data_url)
trainers_df = pd.DataFrame(trainers_json)

trainers_country_counts_df = trainers_df['country'].value_counts().reset_index()
trainers_country_counts_df.columns = ['country', 'count']

# Create bar chart with plotly.graph_objects
fig = go.Figure(data=[
    go.Bar(
        x=trainers_country_counts_df['country'],
        y=trainers_country_counts_df['count'],
        marker_color='steelblue'
    )
])
fig.update_layout(
    title="Count CLDT by Country",
    xaxis_title="Country",
    yaxis_title="Count",
    template="plotly_white"
)



dash.register_page(__name__)

layout = html.Div([
    html.H1('These are our Trainers'),
    html.Div("Some text about the Trainers. They teach our future Instructors."),
    html.Br(),
    html.Div(id='analytics-output'),
        # Display table
    dash_table.DataTable(
        data=trainers_json,  # Pass the list of dictionaries as data
    ),
    # Display bar plot
    dcc.Graph(figure=fig)


]) # close outer html.Div 