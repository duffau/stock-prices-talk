import requests

BASE_URL = "https://www.alphavantage.co/query"

def get_daily_close(symbol, outputsize="compact", datatype="csv", api_key=None):
    func = "TIME_SERIES_DAILY_ADJUSTED"
    query_template = "?function={func}&symbol={symbol}&outputsize={outputsize}&datatype={datatype}&apikey={apikey}"
    query = query_template.format(
        func=func,
        symbol=symbol,
        outputsize=outputsize,
        datatype=datatype,
        apikey=api_key,
    )
    url = BASE_URL + query
    return requests.get(url)


def search(keywords, api_key=None):
    func = "SYMBOL_SEARCH"
    query_template = "?function={func}&keywords={keywords}&apikey={apikey}"
    query = query_template.format(
        func=func,
        keywords=keywords,
        apikey=api_key,
    )
    url = BASE_URL + query
    print(requests.get(url).text)
