#!/usr/bin/env python

import requests
import json
import ConfigParser
import unittest
import os
from datetime import date



# FUNCTION DEFINITIONS

def get_latlon():
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

def get_forecast(url):
    r = requests.get(url)
    return r.content

if __name__ == "__main__":
    apikey = get_apikey()
    latitude, longitude = get_latlon()
    forecast_url = 'https://api.forecast.io/forecast/' + apikey +  '/' + latitude + ',' + longitude
    forecast = json.loads(get_forecast(forecast_url))
    current_conditions = forecast['currently']
    for key, value in current_conditions.iteritems():
        print(key + ':' + str(value))

    daily_forecast_data = forecast['daily']
    daily_forecast = daily_forecast_data['data']
    today = date.today()
    day_offset  = date.weekday(today)
    today_num = date.weekday(today) - day_offset
    print( str(today_num)) 
    print(daily_forecast[today_num])
