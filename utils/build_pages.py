import requests

def get_json_from_url(url):
    r = requests.get(url)
    data = r.json() 
    data = data['query_result']['data']['rows']
    return data 

