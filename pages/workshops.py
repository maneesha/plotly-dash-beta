import dash
from dash import html, dcc, Input, Output, State 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart,  get_country_counts_df, add_hover_text, create_country_counts_map, create_main_table, set_up_search_filter, create_country_counts_table, set_up_download_button, set_up_clear_filters_button
import pandas as pd

page_id = "workshops"

# Initialize page 
dash.register_page(__name__, title="Workshops")

page_header = html.H2("Workshops")

# Load in instructor workshops data as json and df 
workshops_json = get_json_from_query_number(782)
workshops_df = pd.DataFrame(workshops_json)
workshops_df['country'] = workshops_df['country'].replace('', 'Unknown')

# Create country counts df 
# Include column for hover text
workshops_country_counts_df = get_country_counts_df(workshops_df)
workshops_country_counts_df = add_hover_text(workshops_country_counts_df)

# Create full table display
full_table = create_main_table(workshops_df, page_id, 20)

# Set up filters for country
country_filter = set_up_search_filter(workshops_df, page_id, 'country', 'Country') 

# Set up reset button
reset_search = set_up_clear_filters_button(page_id)

# Set up download data button
download_button = set_up_download_button(page_id)

# Create country count table display 
country_count_header = html.H2('Count Trainers by Country')
country_count_table =  create_country_counts_table(workshops_country_counts_df, 15)

# Create country bar chart
country_bar_chart = create_country_bar_chart(workshops_country_counts_df, 'log')
country_bar_chart = dcc.Graph(figure=country_bar_chart, style={'height': '700px', 'width': '100%'})

# Create country counts maps (linear and log scale)
countries_map_linear = create_country_counts_map(workshops_country_counts_df, scale_type='linear')
countries_map_log = create_country_counts_map(workshops_country_counts_df, scale_type='log')

log_map_header = html.H2('Map workshops by country - Log Scale')
log_map = dcc.Graph(figure=countries_map_log,  style={'height': '700px', 'width': '100%'} )

# Set up page layout
layout = html.Div([page_header,
                   country_filter, 
                   reset_search, download_button,
                   full_table, 
                   country_count_table, 
                   country_bar_chart,
                   log_map ])


# Function to activate country and active status filters
@dash.callback(
    Output(f"{page_id}-table", "data"),
    Input(f"{page_id}-country-dropdown", "value")
)
def update_table(country_filter):
    filtered = workshops_df.copy()

    if country_filter:
        filtered = filtered[filtered["country"].isin(country_filter)]

    return filtered.to_dict("records")


# Reset filters to display all data 
@dash.callback(
    Output(f'{page_id}-country-dropdown', 'value'),
    Input(f'{page_id}-clear-filters-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return None


# Downlod current data as csv
@dash.callback(
    Output(f"{page_id}-download-table", "data"),
    Input(f"{page_id}-btn-download", "n_clicks"),
    State(f"{page_id}-table", "data"),
    prevent_initial_call=True
)
def download_filtered_table(n_clicks, table_data):
    filtered_df = pd.DataFrame(table_data)
    return dcc.send_data_frame(filtered_df.to_csv, filename="carpentries_workshop_data.csv")