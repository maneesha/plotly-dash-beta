import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart 
import pandas as pd 


workshops_json = get_json_from_query_number(782)
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