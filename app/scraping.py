import bs4
import urllib.request
import time
import re
import json
import ast
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
GLOBAL_URL = "https://www.worldometers.info/"


def save_to_json_file(data, filename):
    res = dict()
    res['data'] = data
    res['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%SUTC')

    dataJson = json.dumps(res)
    f = open("app/data/" + filename + ".json", "w")
    f.write(dataJson)
    f.close()

# CORONAVIRUS SCRAPING


def fetch_data_coronavirus():
    data = []
    key = ['place', "Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered",
           "New Recovered", "Active Cases", "Critical", "Total Cases/1M pop", "Deaths/1M pop", "Total Tests", "Tests/1M pop", "Population", "Region"]
    req = urllib.request.Request(
        'https://www.worldometers.info/coronavirus/', headers=HEADERS)
    source = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(source, 'html.parser')
    tables = soup.find_all('tbody')
    table_rows = tables[0].find_all('tr')
    i = 0
    for tr in table_rows:
        if i > 6:
            data.append(
                dict(zip(key, re.split('\n', tr.text[1:].replace(" ", ""))[:-2])))
        i += 1

    save_to_json_file(data, "coronavirus")
