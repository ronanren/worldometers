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
    return "<h1>Unofficial Worldometers.info API</h1><p>This site is a API for get data from Worldometers.info</p>"

# CORONAVIRUS SECTION
@app.route('/api/coronavirus/all/', methods=['GET'])
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

    res = dict()
    res['data'] = data
    return res


@app.route('/api/coronavirus/country/<country>', methods=['GET'])
def api_country(country):

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
            if (dict(zip(key, re.split('\n', tr.text[1:])[:-2]))['Country'].lower() == country.lower()):
                data.append(dict(zip(key, re.split('\n', tr.text[1:])[:-2])))
        i += 1

    res = dict()
    res['data'] = data
    return res


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
