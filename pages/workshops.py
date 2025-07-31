import dash
from dash import html, dash_table, dcc, Input, Output, State 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart,  get_country_counts_df, add_hover_text, create_country_counts_map, create_main_table
import pandas as pd

# Initialize page 
dash.register_page(__name__, title="Workshops")

# Load in workshops data as json and df 
workshops_json = get_json_from_query_number(782)
workshops_df = pd.DataFrame(workshops_json)
columns = ['host_organization', 'slug', 'start_date', 'end_date', 'venue', 'country',  'url', 'instructors', 'helpers',  'hosts',  'latitude',  'longitude',]
workshops_df = workshops_df[columns]

# Create country counts df 
# Include column for hover text
workshops_country_counts_df = get_country_counts_df(workshops_df)
workshops_country_counts_df = add_hover_text(workshops_country_counts_df)

# Create country counts bar charts - linear and log scale 
chart_linear = create_country_bar_chart(workshops_country_counts_df, 'linear')
chart_log = create_country_bar_chart(workshops_country_counts_df, 'log')

print(workshops_country_counts_df.dtypes)

# Create country counts map
countries_map_linear = create_country_counts_map(workshops_country_counts_df, scale_type='linear')
countries_map_log = create_country_counts_map(workshops_country_counts_df, scale_type='log')

# Set up building blocks for page layout 
header = html.H1('These are our WONDERFUL Workshops.')
intro_text = html.Div("Something about Workshops. This is a list of DC, LC, SWC workshops.")
search_filter_options =  html.Div([
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
        html.Button("Download the the Filtered CSV", id="btn-download"),
        dcc.Download(id="download-table")

        ], style={"marginBottom": 20, "maxWidth": "400px"})

full_table = create_main_table(workshops_df, "workshops-table", 20)

country_count_header = html.H2('Count Workshops by Country')
country_count_table =  dash_table.DataTable(
        id="country-count-table",
        data=workshops_country_counts_df.to_dict("records"),
        columns=[
            {'name':"country_full_name", 'id':"country_full_name"}, {'name':"count", 'id':"count"}
            ],
        sort_action='native',
        page_size=10,
        fill_width=False
    )


linear_plot_header = html.H2('Plot workshops by country - Linear Scale')
linear_plot = dcc.Graph(figure=chart_linear)

log_plot_header = html.H2('Plot workshops by country - Log Scale')
log_plot = dcc.Graph(figure=chart_log)

linear_map_header = html.H2('Map workshops by country - Linear Scale')
linear_map = dcc.Graph(figure=countries_map_linear,  style={'height': '700px', 'width': '100%'} )

log_map_header = html.H2('Map workshops by country - Log Scale')
log_map = dcc.Graph(figure=countries_map_log,  style={'height': '700px', 'width': '100%'} )

# Set up page layout
layout = html.Div([
    # Page heading 
    header,
    # Page intro text 
    intro_text,
    html.Br(),

    # New div - set up search/filter options
    search_filter_options,

    # Display table
    full_table,

    # Display table for country counts
    country_count_header,
    country_count_table,

    # Display bar plot for country counts 
    linear_plot_header, linear_plot,
    # Display bar plot for country counts 
    log_plot_header, log_plot,

    # Display map for country counts 
    linear_map_header, linear_map,
    log_map_header, log_map 

]) # close outer html.Div 


@dash.callback(
    Output("workshops-table", "data"),
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
    State("workshops-table", "data"),
    prevent_initial_call=True
)
def download_filtered_table(n_clicks, table_data):
    filtered_df = pd.DataFrame(table_data)
    return dcc.send_data_frame(filtered_df.to_csv, filename="carpentries_workshop_data.csv")