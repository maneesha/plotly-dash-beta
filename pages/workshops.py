import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_url, create_country_bar_chart 
import os 
import pandas as pd 

redash_api_key = os.getenv("REDASH_KEY_QUERY782")

redash_data_url = f"http://redash.carpentries.org/api/queries/782/results.json?api_key={redash_api_key}"

workshops_json = get_json_from_url(redash_data_url)
workshops_df = pd.DataFrame(workshops_json)

workshops_country_counts_df = workshops_df['country'].value_counts().reset_index()
workshops_country_counts_df.columns = ['country', 'count']

chart = create_country_bar_chart(workshops_country_counts_df)

dash.register_page(__name__)

layout = html.Div([
    html.H1('These are our Workshops.'),
    html.Div("Something about Workshops. This is a list of DC, LC, SWC workshops."),
    html.Br(),
    html.Div(id='analytics-output'),
        # Display table
    dash_table.DataTable(
        data=workshops_json,  # Pass the list of dictionaries as data
    ),

    # Display bar plot
    dcc.Graph(figure=chart)

]) # close outer html.Div 