import requests
import plotly.graph_objects as go
import os 

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
