import dash
from dash import html, dash_table, dcc 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart 
import pandas as pd 

# Initialize page 
dash.register_page(__name__, title="Workshops")

# Load in workshops data as json and df 
workshops_json = get_json_from_query_number(782)
workshops_df = pd.DataFrame(workshops_json)

# Create country counts df 
workshops_country_counts_df = workshops_df['country'].value_counts().reset_index()

# Create country counts bar chart 
chart = create_country_bar_chart(workshops_country_counts_df)

# Set up page layout
layout = html.Div([
    # Page heading 
    html.H1('These are our Workshops.'),
    # Page intro text 
    html.Div("Something about Workshops. This is a list of DC, LC, SWC workshops."),
    html.Br(),
    # Display table
    dash_table.DataTable(
        data=workshops_json, 
        # Add sort feature to table
        sort_action='native',
        # Set number of rows to display
        page_size=20,
    ),
    # Display bar plot
    html.H2('Plot workshops by country'),
    dcc.Graph(figure=chart)

]) # close outer html.Div 