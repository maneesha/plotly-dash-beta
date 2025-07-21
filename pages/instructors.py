import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_query_number,create_country_bar_chart  
import pandas as pd


instructors_json = get_json_from_query_number(776)
instructors_df = pd.DataFrame(instructors_json)

instructors_country_counts_df = instructors_df['country'].value_counts().reset_index()
instructors_country_counts_df.columns = ['country', 'count']

chart = create_country_bar_chart(instructors_country_counts_df)

dash.register_page(__name__)

layout = html.Div([
    html.H1('These are our Instructors'),
    html.Div("Something about Instructors. They teach DC, LC, SWC workshops."),
    html.Br(),
    html.Div(id='analytics-output'),
        # Display table
    dash_table.DataTable(
        data=instructors_json,  # Pass the list of dictionaries as data
    ),

    dcc.Graph(figure=chart)

]) # close outer html.Div 