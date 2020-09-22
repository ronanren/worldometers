from flask import Flask
from flask_restful import Api
from flask import request, jsonify
from flask import jsonify

from bs4 import BeautifulSoup
import urllib.request
import re
import json
import ast
from cachetools import cached, TTLCache
from apscheduler.schedulers.background import BackgroundScheduler
from app.scraping import fetch_data_coronavirus


app = Flask(__name__)
api = Api(app)
cache = TTLCache(maxsize=1024, ttl=120)


sched = BackgroundScheduler()
sched.add_job(fetch_data_coronavirus, 'interval', minutes=1, max_instances=2)
sched.start()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Unofficial Worldometers.info API</h1><p>This site is a API for get data from Worldometers.info</p>"

# CORONAVIRUS SECTION
@cached(cache)
def get_data_coronavirus():
    f = open('app/coronavirus.json', "r")
    data = f.read()
    data = ast.literal_eval(data)
    f.close()

    return data


@app.route('/api/coronavirus/all/', methods=['GET'])
def api_coronavirus_all():
    res = get_data_coronavirus()
    return res


@app.route('/api/coronavirus/country/<country>', methods=['GET'])
def api_coronavirus_country(country):
    res = get_data_coronavirus()
    i = 1
    found = False
    while (not found and i < len(res['data'])):
        if (res['data'][i]['Country'].lower() == country.lower()):
            found = True
        else:
            i += 1
    if (found):
        return res['data'][i]
    else:
        return {"Error": "Country not found !"}


# POPULATION SECTION
@app.route('/api/population/all/', methods=['GET'])
def api_population():

    data = []
    key = ['Place', "Country", "Population", "Yearly Change (%)", "Net Change", "Density (P/Km*Km)", "Land Area (Km*Km)",
           "Migrants (net)", "Fert Rate", "Median Age", "Urban Pop (%)", "World Share"]
    req = urllib.request.Request('https://www.worldometers.info/world-population/population-by-country/',
                                 headers={'User-Agent': 'Mozilla/5.0'})
    source = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(source, 'html.parser')
    tables = soup.find_all('body')
    table_rows = tables[0].find_all('tr')
    for tr in table_rows[1:]:
        data.append(
            dict(zip(key, re.split(' ', tr.text.replace(" %", "")[1:]))))

    res = dict()
    res['data'] = data
    return res
