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


def create_country_bar_chart(df):
    fig = go.Figure(data=[
        go.Bar(
            x=df['country'],
            y=df['count'],
            marker_color='steelblue'
        )
    ])
    fig.update_layout(
        title="Count by Country",
        xaxis_title="Country",
        yaxis_title="Count",
        template="plotly_white"
    )

    y_max = df['count'].max() * 1.1

    fig.update_yaxes(range=[0, y_max])

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

# Function to add log scale to a dataframe
def add_log_scale(df):
    df['log_count'] = np.log10(df['count'])
    return df

# Function to add hover text to a dataframe
def add_hover_text(df):
    df['hover_text'] = df['country_full_name'] + '<br>Value: ' + df['count'].astype(str)
    return df


