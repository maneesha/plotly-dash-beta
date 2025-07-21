import dash
from dash import html, dash_table
from utils.build_pages import get_json_from_url 
import os 

redash_api_key = os.getenv("REDASH_KEY_QUERY776")

redash_data_url = f"http://redash.carpentries.org/api/queries/776/results.json?api_key={redash_api_key}"

df = get_json_from_url(redash_data_url)

dash.register_page(__name__)

layout = html.Div([
    html.H1('These are our Instructors'),
    html.Div("Something about Instructors. They teach DC, LC, SWC workshops."),
    html.Br(),
    html.Div(id='analytics-output'),
        # Display table
    dash_table.DataTable(
        data=df,  # Pass the list of dictionaries as data
    ),


]) # close outer html.Div 