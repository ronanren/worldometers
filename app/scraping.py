import bs4
import urllib.request
import time
import re
import json
import ast
import os
from datetime import datetime
from selenium import webdriver
from app.constants import HEADERS, GLOBAL_URL, CORONAVIRUS_URL, GOOGLE_CHROME_PATH, CHROMEDRIVER_PATH, DEPLOY

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
    req = urllib.request.Request(CORONAVIRUS_URL, headers=HEADERS)
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


# GLOBAL SCRAPING

def fetch_data_global():
    # Getting the web page
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    if DEPLOY == 'dev':
        driver = webdriver.Chrome(chrome_options=chrome_options)
    else:
        chrome_options.binary_location = GOOGLE_CHROME_PATH
        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    driver.implicitly_wait(30)
    driver.get(GLOBAL_URL)
    driver.implicitly_wait(30)

    # Data processing
    data = dict()
    last_row = ""

    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find('div', 'counterdiv').children

    for row in rows:
        if isinstance(row, bs4.element.Tag):
            if row['class'][0] == 'counter-title' or row['class'][0] == 'counter-title-top':
                data[row.text] = dict()
                last_row = row.text
            elif row['class'][0] == 'counter-group' and row.find('span', 'counter-item') != None:
                data[last_row][row.find(
                    'span', 'counter-item').text] = row.find('span', 'rts-counter').text

    save_to_json_file(data, "global")

    driver.close()
