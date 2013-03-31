#!/usr/bin/env python

import requests
import json
import ConfigParser
import unittest
import os
from datetime import date



# FUNCTION DEFINITIONS
def get_latlon_from_file():
    '''Reads in configuration file.''' 
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.weatherreport.cfg'), 
        '/etc/weatherreport.cfg', 'weatherreport.cfg'])
    if config.has_section('location'):
        latitude =  config.get('location', 'latitude')
        longitude =  config.get('location', 'longitude')
    return latitude, longitude

def get_apikey():
    f = open(os.path.expanduser('~/forecast.io.api.key'), 'r')
    key = f.readline()
    f.close()
    return key.rstrip()

def get_days():
    '''returns a list of days of the week as  integers, 
    where Monday is 0 and Sunday is 6,
    and days[0] = today e.g. if today is Tuesday days[0] == 1   
    corresponds to datetime.date.weekday()'''
    today = date.today()
    tnum = today.weekday()
    days = []
    for i in range(7):
        x = tnum + i
        if x <= 7:
            days.append(x)
        else:
            days.append(x - 8)
    return days
    
def get_forecast(url):
    r = requests.get(url)
    return json.loads(r.content)


# class definition
class ForecastNow():
    def __init__(self, apikey, lat, lon):
        self.apikey = apikey
        self.lat = lat
        self.lon = lon
        self.url = 'https://api.forecast.io/forecast/' + apikey +  '/' + lat + ',' + lon
    def load_forecast(self):
        self.forecast = get_forecast(self.url)
        self.current = self.forecast['currently']
        _daily_data = self.forecast['daily']
        self.daily = _daily_data['data']

if __name__ == "__main__":
    apikey = get_apikey()
    latitude, longitude = get_latlon_from_file()
    todays_weather = ForecastNow(apikey, latitude, longitude)
    todays_weather.load_forecast()
    current_conditions = todays_weather.current
    for key, value in current_conditions.iteritems():
        print(key + ':' + str(value))

