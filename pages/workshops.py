import dash
from dash import html, dash_table, dcc, Input, Output, State 
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

    # New div - set up search/filter options
    html.Div([
        # Inner div for search 
        html.Div([html.Label("Search by Name:"),
                  dcc.Input(id="name-search", type="text", placeholder="Type name...", debounce=True),]),

        # Inner div for country filter 
        html.Div([html.Label("Filter by Country:"),
                  dcc.Dropdown(
                        id="country-dropdown",
                        options=[{"label": c, "value": c} for c in sorted(workshops_df["country"].unique())],
                        multi=True,
                        placeholder="Select country..."
                ),],),
    
        # Download button 
        html.Button("Download Filtered CSV", id="btn-download"),
        dcc.Download(id="download-table")

        ], style={"marginBottom": 20, "maxWidth": "400px"}),


    # Display table
    dash_table.DataTable(
        id="all-workshops-table",
        data=workshops_json, 
        # Add sort feature to table
        sort_action='native',
        # Set number of rows to display
        page_size=20,
    ),

    # Display table for country counts
    html.H2('Count Workshops by Country'),
    dash_table.DataTable(
        id="country-count-table",
        data=workshops_country_counts_df.to_dict("records"),
        sort_action='native',
        page_size=10,
    ),

    # Display bar plot for country counts 
    html.H2('Plot workshops by country'),
    dcc.Graph(figure=chart)

]) # close outer html.Div 


@dash.callback(
    Output("all-workshops-table", "data"),
    Input("name-search", "value"),
    Input("country-dropdown", "value")
)
def update_table(name_search, country_filter):
    filtered = workshops_df.copy()

    if name_search:
        filtered = filtered[filtered["instructors"].str.contains(name_search, case=False, na=False)]

    if country_filter:
        filtered = filtered[filtered["country"].isin(country_filter)]

    return filtered.to_dict("records")


@dash.callback(
    Output("download-table", "data"),
    Input("btn-download", "n_clicks"),
    State("table", "data"),
    prevent_initial_call=True
)
def download_filtered_table(n_clicks, table_data):
    filtered_df = pd.DataFrame(table_data)
    return dcc.send_data_frame(filtered_df.to_csv, filename="carpentries_workshop_data.csv")