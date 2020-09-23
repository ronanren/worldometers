from bs4 import BeautifulSoup
import urllib.request
import re
import json
import ast
from datetime import datetime


def fetch_data_coronavirus():
    data = []
    key = ['place', "Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered",
           "New Recovered", "Active Cases", "Critical", "Total Cases/1M pop", "Deaths/1M pop", "Total Tests", "Tests/1M pop", "Population", "Region"]
    req = urllib.request.Request('https://www.worldometers.info/coronavirus/',
                                 headers={'User-Agent': 'Mozilla/5.0'})
    source = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(source, 'html.parser')
    tables = soup.find_all('tbody')
    table_rows = tables[0].find_all('tr')
    i = 0
    for tr in table_rows:
        if i > 6:
            data.append(
                dict(zip(key, re.split('\n', tr.text[1:].replace(" ", ""))[:-2])))
        i += 1

    res = dict()
    res['data'] = data
    res['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    dataJson = json.dumps(res)
    f = open("app/data/coronavirus.json", "w")
    f.write(dataJson)
    f.close()
