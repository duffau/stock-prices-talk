import requests

def real_gdp_world():
    url = "http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.KD?downloadformat=csv"
    return requests.get(url).text
    