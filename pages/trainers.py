import dash
from dash import html, dash_table, dcc, Input, Output, State 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart,  get_country_counts_df, add_hover_text, create_country_counts_map, create_main_table, set_up_search_filter, create_country_counts_table, set_up_download_button
import pandas as pd


# Initialize page 
dash.register_page(__name__, title="Instructor Trainers")

# Load in instructor trainers data as json and df 
trainers_json = get_json_from_query_number(775)
trainers_df = pd.DataFrame(trainers_json)

# Create country counts df 
# Include column for hover text
trainers_country_counts_df = get_country_counts_df(trainers_df)
trainers_country_counts_df = add_hover_text(trainers_country_counts_df)

# Create full table display
full_table = create_main_table(trainers_df, "trainers-table", 20)

# Set up filters for active status and country
active_filter =  set_up_search_filter(trainers_df, 'active_status', 'Active Status') 
country_filter = set_up_search_filter(trainers_df, 'country', 'CounTRY') 

# Set up reset button
reset_search = html.Button('Clear All Filters', id='clear-filters-button')

# Set up download data button
download_button = set_up_download_button()

# Create country count table display 
country_count_header = html.H2('Count Trainers by Country')
country_count_table =  create_country_counts_table(trainers_country_counts_df, 15)

# Create country counts maps (linear and log scale)
countries_map_linear = create_country_counts_map(trainers_country_counts_df, scale_type='linear')
countries_map_log = create_country_counts_map(trainers_country_counts_df, scale_type='log')

log_map_header = html.H2('Map workshops by country - Log Scale')
log_map = dcc.Graph(figure=countries_map_log,  style={'height': '700px', 'width': '100%'} )

# Set up page layout
layout = html.Div(["hello world", 
                   country_filter, 
                   active_filter, 
                   reset_search, download_button,
                   full_table, 
                   country_count_table, 
                   log_map ])

# Function to activate country and active status filters
@dash.callback(
    Output("trainers-table", "data"),
    Input("active_status-dropdown", "value"),
    Input("country-dropdown", "value")
)
def update_table(active_filter, country_filter):
    filtered = trainers_df.copy()

    if country_filter:
        filtered = filtered[filtered["country"].isin(country_filter)]

    if active_filter:
        filtered = filtered[filtered["active_status"].isin(active_filter)]

    return filtered.to_dict("records")


# Reset filters to display all data 
@dash.callback(
    Output('active_status-dropdown', 'value'),
    Output('country-dropdown', 'value'),
    Input('clear-filters-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return None, None

# Downlod current data as csv
@dash.callback(
    Output("download-table", "data"),
    Input("btn-download", "n_clicks"),
    State("trainers-table", "data"),
    prevent_initial_call=True
)
def download_filtered_table(n_clicks, table_data):
    filtered_df = pd.DataFrame(table_data)
    return dcc.send_data_frame(filtered_df.to_csv, filename="carpentries_workshop_data.csv")