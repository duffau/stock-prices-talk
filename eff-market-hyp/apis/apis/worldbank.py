import requests

BASE_URL = "http://api.worldbank.org/v2/en/indicator"


def get_indicator(indicator, location=None, format="csv"):
    if location:
        url = f"{BASE_URL}/{indicator}?downloadformat={format}"
    else:
        url = f"{BASE_URL}/{indicator}?location={location}&downloadformat={format}"
    return requests.get(url).text

def real_gdp(country_code=None):
    return get_indicator("NY.GDP.MKTP.KD", location=country_code)


def gdp_inflation(country_code=None):
    return get_indicator("NY.GDP.DEFL.KD.ZG", location=country_code)


def cpi_inflation(country_code=None):
    return get_indicator("FP.CPI.TOTL.ZG", location=country_code)
