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
from app.scraping import fetch_data_global


app = Flask(__name__)
api = Api(app)
cacheCovid = TTLCache(maxsize=1024, ttl=30)
cacheGlobal = TTLCache(maxsize=1024, ttl=30)

sched = BackgroundScheduler()
sched.add_job(fetch_data_coronavirus, 'interval', minutes=1, max_instances=2)
sched.add_job(fetch_data_global, 'interval', minutes=0.1, max_instances=2)
sched.start()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Unofficial Worldometers.info API</h1><p>This site is a API for get data from Worldometers.info</p>"


# CORONAVIRUS SECTION
@cached(cacheCovid)
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

# GLOBAL SECTION
@cached(cacheGlobal)
def get_data_global():
    f = open('app/data/global.json', "r")
    data = f.read()
    data = ast.literal_eval(data)
    f.close()
    return data


def get_specific_data_global(specification):
    res = {}
    data = get_data_global()
    res['data'] = data['data'][specification]
    res['last_update'] = data['last_update']
    return res


@app.route('/api/global/all/', methods=['GET'])
def api_global_all():
    res = get_data_global()
    return res


@app.route('/api/global/world-population/', methods=['GET'])
def api_global_world_population():
    return get_specific_data_global("World Population")


@app.route('/api/global/government-economics/', methods=['GET'])
def api_global_government_economics():
    return get_specific_data_global("Government & Economics")


@app.route('/api/global/society-media/', methods=['GET'])
def api_global_society_media():
    return get_specific_data_global("Society & Media")


@app.route('/api/global/environment/', methods=['GET'])
def api_global_environment():
    return get_specific_data_global("Environment")


@app.route('/api/global/food/', methods=['GET'])
def api_global_food():
    return get_specific_data_global("Food")


@app.route('/api/global/water/', methods=['GET'])
def api_global_water():
    return get_specific_data_global("Water")


@app.route('/api/global/energy/', methods=['GET'])
def api_global_energy():
    return get_specific_data_global("Energy")


@app.route('/api/global/health/', methods=['GET'])
def api_global_health():
    return get_specific_data_global("Health")
