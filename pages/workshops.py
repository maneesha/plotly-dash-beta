import dash
from dash import html, dash_table, dcc, Input, Output, State 
from utils.build_pages import get_json_from_query_number, create_country_bar_chart, get_country_counts_df, add_log_scale, add_hover_text 
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Initialize page 
dash.register_page(__name__, title="Workshops")

# Load in workshops data as json and df 
workshops_json = get_json_from_query_number(782)
workshops_df = pd.DataFrame(workshops_json)

# Create country counts df 
# Include columns for log scale and hover text
workshops_country_counts_df = get_country_counts_df(workshops_df)
workshops_country_counts_df = add_log_scale(workshops_country_counts_df)
workshops_country_counts_df = add_hover_text(workshops_country_counts_df)

# Create country counts bar chart 
chart = create_country_bar_chart(workshops_country_counts_df)


chart_log = go.Figure(data=[
    go.Bar(
        x=workshops_country_counts_df['country'],
        y=workshops_country_counts_df['log_count'],
        marker_color='steelblue',
        text=workshops_country_counts_df['count'],
        hovertemplate='<b>%{x}</b><br>Value: %{text}<extra></extra>'
    )
    ])

tick_vals = [100, 200, 500, 1000, 2000]
tick_text = [str(v) for v in tick_vals]
chart_log.update_layout(
    yaxis=dict(
        type='log',
        title='Value',
        tickvals=tick_vals,
        ticktext=tick_text
    ),
)


# Create country counts map

## LINEAR SCALE MAP
countries_map = go.Figure(data=go.Choropleth(
    locations = workshops_country_counts_df['country_alpha3'],
    z = workshops_country_counts_df['count'],
    colorscale = 'Blues',
    colorbar = dict(
        title = 'Value',
        tickvals = [100, 500, 1000, 1500, 2000],
        ticktext = [100, 500, 1000, 1500, 2000],),
    autocolorscale=False, # Do not automatically apply colorscale
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Workshop count',
    text = workshops_country_counts_df['hover_text'], # custom hover text
    hovertemplate = '%{text}<extra></extra>',
))
countries_map.update_geos(projection_type='natural earth',)
## END LINEAR SCALE MAP 


## LOG SCALE MAP 
countries_map_log = go.Figure(data=go.Choropleth(
    locations = workshops_country_counts_df['country_alpha3'],
    z = workshops_country_counts_df['log_count'],
    # text = df_log['country_full_name'],
    colorscale = 'Blues',
    colorbar = dict(
        title = 'Value',
        tickvals = [np.log10(v) for v in [25, 50, 100, 300, 1000, 2000]],
        ticktext = ['25', '50', '100', '300', '1000', '2000']),
    autocolorscale=False, # Do not automatically apply colorscale
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'Workshop count',
    text = workshops_country_counts_df['hover_text'], # custom hover text
    hovertemplate = '%{text}<extra></extra>',
))
countries_map_log.update_geos(projection_type='natural earth',)
## END LOG SCALE MAP 

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
    html.H2('Plot workshops by country - Linear Scale'),
    dcc.Graph(figure=chart),
    # Display bar plot for country counts 
    html.H2('Plot workshops by country - Log Scale'),
    dcc.Graph(figure=chart_log),

    # Display map for country counts 
    html.H2('Map workshops by country - Linear Scale'),
    dcc.Graph(figure=countries_map,  style={'height': '700px', 'width': '100%'} ),

    html.H2('Map workshops by country - Log Scale'),
    dcc.Graph(figure=countries_map_log,  style={'height': '700px', 'width': '100%'} ),

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