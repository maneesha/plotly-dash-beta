import dash
from dash import html, dash_table
from utils.build_pages import get_json_from_url 
import os 
import pandas as pd 

redash_api_key = os.getenv("REDASH_KEY_QUERY523")

redash_data_url = f"http://redash.carpentries.org/api/queries/523/results.json?api_key={redash_api_key}"

trainers_json = get_json_from_url(redash_data_url)
trainers_df = pd.DataFrame(trainers_json)

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


]) # close outer html.Div 