from flask import Flask
from flask_restful import Api
from flask import request, jsonify

from bs4 import BeautifulSoup
import urllib.request
from flask import jsonify
import re


app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Unofficial Worldometers.info API</h1><p>This site is a prototype API for get data from Worldometers.info</p>"


@app.route('/api/coronavirus/', methods=['GET'])
def api_all():

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
            data.append(dict(zip(key, re.split('\n', tr.text[1:])[:-2])))
        i += 1

    return jsonify(data)


app.run(debug=True)
