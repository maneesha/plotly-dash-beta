import requests
import plotly.graph_objects as go
import os
import pycountry
import numpy as np
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc



def get_json_from_query_number(query_number):
    """
    Takes one argument: Redash query number as int 
    Returns the data as a list of dicts.

    Requires the env variable REDASH_KEY_QUERY{query_number} to be set.
    """

    redash_api_key = os.getenv(f"REDASH_KEY_QUERY{query_number}")
    redash_data_url = f"http://redash.carpentries.org/api/queries/{query_number}/results.json?api_key={redash_api_key}"

    r = requests.get(redash_data_url)
    data = r.json() 
    data = data['query_result']['data']['rows']
    return data 


def create_country_bar_chart(df, scale_type):
    """
    Takes two arguments: dataframe and scale type ('linear' or 'log').

    Returns a Plotly bar chart figure.
    """

    # Intialize figure 
    fig = go.Figure()

    # Add bar chart trace
    fig.add_trace(go.Bar(x=df['country'],
                         y=df['count'],
                         text=df['count'],
                         customdata=df[['country_full_name']],
                         hovertemplate="<b>%{customdata[0]}</b>: %{text}<extra></extra>"))

    # Set y-ticks based on scale type 
    if scale_type == 'linear':
        tick_vals =[0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
    elif scale_type == 'log':
        tick_vals = [1, 10, 50, 100, 500, 1000, 2000, 5000]

    # Update yticks.  Auto or array to use above defined lists
    fig.update_layout(
        yaxis=dict(
            type=scale_type,  # Set y-axis to log or linear scale
            # tickmode='auto',  # Use 'array' for custom tick values
            tickvals= tick_vals,  # Specify tick values
            # ticktext=[]  List of equivalent length 
        ),
        title=f'Count by Country ({scale_type} scale)',)

    return fig 


def get_country_name(code):
    """
    Takes one argument: alpha-2 country code as string.
    Returns the full country name as a string.
    """
    
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return "Country unknown"


def get_country_alpha3(code):
    """
    Takes one argument: alpha-2 country code as string.
    Returns the alpha-3 country code as a string.
    """
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return "Country unknown"


def get_country_counts_df(df):
    """
    Takes one argument: dataframe with a 'country' column containing the two character country code.
    Returns a dataframe with country counts, full name and alpha-3 code.
    """
    country_counts_df = df['country'].value_counts().reset_index()
    country_counts_df['country_full_name'] = country_counts_df['country'].apply(get_country_name)
    country_counts_df['country_alpha3'] = country_counts_df['country'].apply(get_country_alpha3)
    return country_counts_df


def add_hover_text(df):
    """
    Takes one argument: dataframe with 'country_full_name' and 'count' columns.
    Returns the dataframe with 'hover_text' column added.
    """

    df['hover_text'] = df['country_full_name'] + '<br>Value: ' + df['count'].astype(str)
    return df


def create_country_counts_map(df, scale_type='linear'):
    """
    Takes two arguments: dataframe with country_alpha3, count, and hover_text columns, and scale type ('linear' or 'log').
    Returns a Plotly choropleth map figure.
    """

    if scale_type == 'linear':
        z = df['count']
        tickvals = [100, 500, 1000, 1500, 2000]
        ticktext = [100, 500, 1000, 1500, 2000]
    elif scale_type == 'log':
        z = np.log10(df['count'])
        tickvals = [np.log10(v) for v in [25, 50, 100, 300, 1000, 2000]]
        ticktext = ['25', '50', '100', '300', '1000', '2000']

    # Create choropleth map
    fig = go.Figure(data=go.Choropleth(
        locations=df['country_alpha3'],
        z=z,
        colorscale='Blues',
        colorbar=dict(title='Value', tickvals=tickvals, ticktext=ticktext),
        autocolorscale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        text=df['hover_text'],
        hovertemplate='%{text}<extra></extra>',
    ))

    fig.update_geos(projection_type='natural earth', landcolor="LightGray", showcountries=True,)
    fig.update_layout(title=f'Count by Country ({scale_type} scale)',)

    return fig


def create_main_table(df, page_id, page_size=20):
    """
    Takes three arguments: dataframe, page_id, and page_size
    Returns a Dash DataTable based on the dataframe.
    """

    return dash_table.DataTable(
        id=f"{page_id}-table",
        data=df.to_dict("records"),
        # Add sort feature to table
        sort_action='native',
        # Set number of rows to display
        page_size=page_size,
        style_cell={'textAlign': 'left'},
        style_table={'overflowX':'scroll'}
    )


def set_up_search_filter(df, page_id, column_name_df, column_name_human):
    """
    Takes four arguments: dataframe, page_id, column name in dataframe, and human-readable column name.
    Returns a Dash HTML Div dropdown to filter by the specified column.
    """

    search_filter = html.Div([
        html.Div([html.Label(f"Filter by {column_name_human}:"),
                  dcc.Dropdown(
                        id=f"{page_id}-{column_name_df}-dropdown",
                        options=[{"label": c, "value": c} for c in sorted(df[f"{column_name_df}"].unique())],
                        multi=True,
                        placeholder=f"Select {column_name_human}..."
                ),],),

        ], style={"marginBottom": 20, "maxWidth": "400px"})
    
    return search_filter


def create_country_counts_table(df, page_size):
    """
    Takes two arguments: dataframe with 'country_full_name' and 'count' columns, and page size.
    Returns a Dash DataTable displaying country counts.
    """

    table = dash_table.DataTable(
        id="country-count-table",
        data=df.to_dict("records"),
        columns=[
            {'name':"country_full_name", 'id':"country_full_name"}, {'name':"count", 'id':"count"}
            ],
        sort_action='native',
        page_size=page_size,
        fill_width=False
    )

    return table


def set_up_download_button(page_id):
    """
    Takes one argument: page_id.
    Returns a Dash HTML Div button and Dash component to download the current data 
    """

    button = dbc.Button("Download current data", id=f"{page_id}-btn-download")
    download = dcc.Download(id=f"{page_id}-download-table")
    return html.Div([button, download])


def set_up_clear_filters_button(page_id):
    """
    Takes one argument: page_id.
    Returns a Dash HTML Div button and Dash component to clear all filters. 
    """

    button = dbc.Button("Clear All Filters", id=f"{page_id}-clear-filters-button")
    return button
