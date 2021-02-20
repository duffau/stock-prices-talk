import requests
import time

def get_historical_data(symbol, api_key):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v3/get-historical-data"

    querystring = {"symbol":symbol, "region":"US"}

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        }

    return requests.get(url, headers=headers, params=querystring).json()

def get_historical_data_v7(symbol):                                                                                             
    url = "https://query1.finance.yahoo.com/v7/finance/download"
    url = "/".join([url, symbol])
    query_params = {
        "period1":-1325635200,
        "period2": int(time.time()),
        "interval":"1d",
        "events": "history", 
        "includeAdjustedClose": "true"
    }
    return requests.get(url, params=query_params).text
