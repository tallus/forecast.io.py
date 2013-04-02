#!/usr/bin/env python
# -*- coding: utf-8 -*-

from forecastio import Forecast
from forecastio import get_days, get_timestamp, from_timestamp, printuc
import ConfigParser
import os
import datetime
from calendar import day_name, day_abbr    
# FUNCTION DEFINITIONS

def get_latlon_from_file(latlonfile = None):
    '''Reads in configuration file.''' 
    config = ConfigParser.ConfigParser()
    if latlonfile:
        config.read(latlonfile)
    else:
        config.read([os.path.expanduser('~/.weatherreport.cfg'), 
            '/etc/weatherreport.cfg', 'weatherreport.cfg'])
    if config.has_section('location'):
        latitude =  config.get('location', 'latitude')
        longitude =  config.get('location', 'longitude')
    return latitude, longitude

def get_apikey_from_file(keyfile = None):
    if keyfile:
        f = open(keyfile, r)
    else:
        f = open(os.path.expanduser('~/forecast.io.api.key'), 'r')
    key = f.readline()
    f.close()
    return key.rstrip()


if __name__ == "__main__":
    units = 'si'
    apikey = get_apikey_from_file()
    latitude, longitude = get_latlon_from_file()
    
    time = get_timestamp(1968,01,07,02,30)
    weather = Forecast(apikey, 'uk', 51.8965, 2.0784, time)
    
    if weather.get_forecast():
        dt = from_timestamp(weather.time)
        printuc('keys present: ' +' '.join(weather.forecast.keys()))
        print('conditions at ' + dt.isoformat(' ') +', ' 
                +  str(weather.latitude) +' N ' + str(weather.longitude) + ' W')
        for key, value in weather.current.iteritems():
            printuc (key +': ' + str(value))
    else:
        print('No Forecast')
    
    print("\n========================================\n")

    todays_weather = Forecast(apikey, units, latitude, longitude)

    if todays_weather.get_forecast():
        printuc("Weekly summary for the next 7 days:\n" 
                + todays_weather.daily['summary'])
        
        heading = [' ', 'Min Temp', 'Max Temp', 'Rain %', 'Summary']
        print(' '.join(('%*s' % (10, x) for x in heading)))
    
        days=get_days()
        for i in range(7):
            day = days[i]
            wdata = todays_weather.daily_data[i]
            if 'precipProbability' in wdata:
                precip = str(wdata['precipProbablity'] * 100) + '%'
            else:
                precip = '-'
            line = [day_abbr[day], str(wdata['temperatureMin']) + u'\xb0C',
                    str(wdata['temperatureMax']) + u'\xb0C', precip, wdata['summary']]
            print(' '.join(('%*s' % (10, x) for x in line)))
    
    else:
        print('No Forecast')
