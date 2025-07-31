import requests
import plotly.graph_objects as go
import os
import pycountry
import numpy as np


def get_json_from_query_number(query_number):
    redash_api_key = os.getenv(f"REDASH_KEY_QUERY{query_number}")
    redash_data_url = f"http://redash.carpentries.org/api/queries/{query_number}/results.json?api_key={redash_api_key}"

    r = requests.get(redash_data_url)
    data = r.json() 
    data = data['query_result']['data']['rows']
    return data 


def create_country_bar_chart(df, scale_type):
    """
    Create bar chart from dataframe containing country counts.
    Allows for different scale types (linear or log).
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


# Function to get full country name from alpha-2 code
def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_2=code).name
    except:
        return "Country unknown"


# Function to get alpha-3 code from alpha-2 code
def get_country_alpha3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return "Country unknown"


# Function to create country counts dataframe 
def get_country_counts_df(df):
    country_counts_df = df['country'].value_counts().reset_index()
    country_counts_df['country_full_name'] = country_counts_df['country'].apply(get_country_name)
    country_counts_df['country_alpha3'] = country_counts_df['country'].apply(get_country_alpha3)
    return country_counts_df


# Function to add hover text to a dataframe
def add_hover_text(df):
    df['hover_text'] = df['country_full_name'] + '<br>Value: ' + df['count'].astype(str)
    return df


def create_country_counts_map(df, scale_type='linear'):
    """
    Create a choropleth map of country counts.
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

    fig.update_geos(projection_type='natural earth', landcolor="LightGray",)

    return fig
