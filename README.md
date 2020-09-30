# Worldometers 🦠

<h4 align="center">Unofficial API from worldometers.info to get coronavirus real-time data</h4>

<p align="center">
<a href="https://badge.fury.io/py/Flask"><img src="https://badge.fury.io/py/Flask.svg" alt="PyPI version" height="18"></a>
<a href="https://badge.fury.io/py/requests"><img src="https://badge.fury.io/py/requests.svg" alt="PyPI version" height="18"></a>
<a href="https://badge.fury.io/py/beautifulsoup4"><img src="https://badge.fury.io/py/beautifulsoup4.svg" alt="PyPI version" height="18"></a>
</p>

<p align="center">
  <a href="#Features">Features</a> |
  <a href="#Usage">Usage</a> |
  <a href="#Installation">Installation</a> |
  <a href="#License">License</a> |
  <a href="#Contact">Contact</a> | 
  <a href="https://ronanren.github.io" target="_blank">My Portfolio</a> 
</p>

# Features

- 🔁 Data update every minute
- 🌎 Get information on every country in the world
- ⌛ API fast with < 200ms
- ☕️ Simple data and simple to use

# Usage

## GET /all

Get all data in real time about coronavirus ranked by country and world from worldometers

**Endpoint** : [https://worldometer.herokuapp.com/api/coronavirus/all/](https://worldometer.herokuapp.com/api/coronavirus/all/)

<details>
<summary><b>Response</b></summary>

```json
{
  "data": [
    {
      "Active Cases": "7,501,542",
      "Country": "World",
      "Critical": "63,266",
      "Deaths/1M pop": "126.4",
      "New Cases": "+220,608",
      "New Deaths": "+3,943",
      "New Recovered": "+149,408",
      "Population": "",
      "Region": "All",
      "Tests/1M pop": "",
      "Total Cases": "32,306,913",
      "Total Cases/1M pop": "4,145",
      "Total Deaths": "985,224",
      "Total Recovered": "23,820,147",
      "Total Tests": "",
      "place": ""
    },
    {
      "Active Cases": "2,539,168",
      "Country": "USA",
      "Critical": "14,090",
      "Deaths/1M pop": "625",
      "New Cases": "+20,681",
      "New Deaths": "+489",
      "New Recovered": "+15,077",
      "Population": "331,452,210",
      "Region": "NorthAmerica",
      "Tests/1M pop": "305,237",
      "Total Cases": "7,160,234",
      "Total Cases/1M pop": "21,603",
      "Total Deaths": "207,082",
      "Total Recovered": "4,413,984",
      "Total Tests": "101,171,573",
      "place": "1"
    },
    {...}
  ],
  "last_update": "2020-09-24 19:00:44"
}
```

</details>

---

## GET /world

Get all data in real time about coronavirus of the world from worldometers

**Endpoint** : [https://worldometer.herokuapp.com/api/coronavirus/world/](https://worldometer.herokuapp.com/api/coronavirus/world/)

<details>
<summary><b>Response</b></summary>

```json
{
  "data": {
    "Active Cases": "7,494,048",
    "Country": "World",
    "Critical": "63,266",
    "Deaths/1M pop": "126.4",
    "New Cases": "+212,867",
    "New Deaths": "+3,696",
    "New Recovered": "+149,408",
    "Population": "",
    "Region": "All",
    "Tests/1M pop": "",
    "Total Cases": "32,299,172",
    "Total Cases/1M pop": "4,144",
    "Total Deaths": "984,977",
    "Total Recovered": "23,820,147",
    "Total Tests": "",
    "place": ""
  },
  "last_update": "2020-09-24 18:49:43"
}
```

</details>

---

## GET /country/{country}

Get all data in real time about coronavirus from one country from worldometers

**Endpoint** : [https://worldometer.herokuapp.com/api/coronavirus/country/{country}](https://worldometer.herokuapp.com/api/coronavirus/country/{country})

<details>
<summary><b>Response</b></summary>

```json
{
  "data": {
    "Active Cases": "371,313",
    "Country": "France",
    "Critical": "1,048",
    "Deaths/1M pop": "483",
    "New Cases": "+16,096",
    "New Deaths": "+52",
    "New Recovered": "+875",
    "Population": "65,307,193",
    "Region": "Europe",
    "Tests/1M pop": "153,664",
    "Total Cases": "497,237",
    "Total Cases/1M pop": "7,614",
    "Total Deaths": "31,511",
    "Total Recovered": "94,413",
    "Total Tests": "10,035,395",
    "place": "11"
  },
  "last_update": "2020-09-24 19:00:44"
}
```

</details>

# Installation

```sh
pip install -r requirements.txt
python run.py
```

# License

<a href="https://github.com/ronanren/Covid19bot/blob/master/LICENSE" target="_blank">MIT</a>

# Contact

**Twitter** : <a href="https://twitter.com/Ronanren" target="_blank">@Ronanren</a>
