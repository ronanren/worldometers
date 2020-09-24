from flask import Flask
from flask_restful import Api
from flask import request, jsonify
from flask import jsonify

from bs4 import BeautifulSoup
import urllib.request
import re
import json
import ast
from datetime import datetime
from cachetools import cached, TTLCache
from apscheduler.schedulers.background import BackgroundScheduler
from app.scraping import fetch_data_coronavirus


app = Flask(__name__)
api = Api(app)
cache = TTLCache(maxsize=1024, ttl=30)

sched = BackgroundScheduler()
sched.add_job(fetch_data_coronavirus, 'interval', minutes=1, max_instances=2)
sched.start()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Unofficial Worldometers.info API</h1><p>This site is a API for get data from Worldometers.info</p>"


# CORONAVIRUS SECTION
@cached(cache)
def get_data_coronavirus():
    f = open('app/data/coronavirus.json', "r")
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
    result = {}
    res = get_data_coronavirus()
    i = 1
    found = False
    while (not found and i < len(res['data'])):
        if (res['data'][i]['Country'].lower() == country.lower()):
            found = True
        else:
            i += 1
    if (found):
        result['data'] = res['data'][i]
        result['last_update'] = res['last_update']
        return result
    else:
        return {"Error": "Country not found !"}


@app.route('/api/coronavirus/world/', methods=['GET'])
def api_coronavirus_world():
    res = {}
    data = get_data_coronavirus()
    res['data'] = data['data'][0]
    res['last_update'] = data['last_update']
    return res
