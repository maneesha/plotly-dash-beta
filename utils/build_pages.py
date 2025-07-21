import requests
import plotly.graph_objects as go


def get_json_from_url(url):
    r = requests.get(url)
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
