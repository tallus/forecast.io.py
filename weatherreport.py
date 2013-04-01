#!/usr/bin/env python

import unittest
import requests
import json
import ConfigParser
import os
import datetime
from datetime import date
from datetime import datetime
from calendar import timegm
import pytz
from pytz import timezone
from time import mktime

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

def get_timestamp(year, month, day, hour = None ,minute = None, second = None, timezone = None):
    '''Returns the number of seconds since Jan 1 1970. 
    Hour, minute, second are optional.
    Timezone is optional and supplied as a string (not a timezone object).
    Naive local time is assumed if timezone is not supplied. '''
    if timezone:
        tz = timezone(timezone)
        dt = tz.localize(datetime(year, month, day, hour, minute, second))
        return timegm(dt.utctimetuple())
    else
        dt = datetime(year, month, day, hour, minute, second))
        return int(time.mktime(dt.timetuple()))

def from_timestamp(timestamp, timezone = None):
    ''''Returns a datetime.datetime object given a timestamp
    Timezone is optional and supplied as a string (not a timezone object).
    Naive local time is assumed if timezone is not supplied. '''
    if timezone:
        tz = timezone(timezone)
        ts= datetime.utcfromtimestamp(timestamp).replace(tzinfo=utc)
        return tz.normalize(ts.astimezone(tz))
    else:
        return datetime.fromtimestamp(timestamp)

# CLASS DEFINITIONS

class Forecast():
    ''' Base class for forecasts using the forecast.io api
    You should generally use the ForecastNow or ForecastTime child classes
    to fetch a forecast/weather record, as this returns the entire forecast'''
    def __init__(self, apikey, units, latitude, longitude, time = None):
        self.apikey = apikey
        self.units = units
        self.lat = latitude
        self.lon = longitude
        self.time = time
        if time:
            self.url = 'https://api.forecast.io/forecast/' + apikey +  '/' + latitude + ',' + longitude + ',' + time + "?units=" + units
        else:
            self.url = 'https://api.forecast.io/forecast/' + apikey +  '/' + latitude + ',' + longitude + "?units=" + units

    def load_forecast(self):
        try:
            r = requests.get(self.url)
        except:
            return False
        else:
            self.forecast = json.loads(r.content)
            return True

class ForecastNow(Forecast):
    ''' Creates an object containg the various forecasts for the present 
    moment in time for the specified latitude and longitude. 
    You will need to call the get_forecast method in order to fetch the data.
    The Forecasts are:
    self.current:           A list containing the current conditions at the 
                            latitude and longtitude specified.
    self.nexthour:          Forecast for the next hour, minute by minute.
                            A list containing:
                            summary -   a human readable summary of the forecast
                            icon    -   a machine readable version of the above
                            data    -   see below.
    self.nexthour_data:     A list of dictionaries containing the actual data
                            The contents of the dictionary may vary but
                            sould at least contain a time field (as unix time)
                            may contain gaps.
    self.hourly             As above. Hour by hour for the next 48 hours
    self.hourly_data
    self.daily              As above. Day by day for the the next 7 days
    self.daily_data     
    self.alerts             Any severe weather warnings issued. A list of
                            dictionaries contains:
                            title:      short text sumamry
                            expires:    unix time the warning expires
                            uri:        url that contains detailed info
    self.flags              Meta data such as source of data see:
                            https://developer.darkskyapp.com/docs/v2
    
    N.B. Any one data set (current, nexthour, hourly, daily, alerts, flags) 
    may or may not be present. In determining a forecast you should check
    to see what if it is available at the most accurate level and fall back
    to the next most accurate if not. In particular it appears that nexthour
    is often  missing or lacking data. Alerts will only be present if there
    are actual alerts. No exceptions will be raised if data is missing.

    The class takes the following parameters:
    apikey, units , latitude, longitude
    units is one of us,si or uk. 
    us gives Imperial measurements, si metric. uk is as si except for wind speed
    in miles per hour.
    Example:

    todays_weather = ForecastNow(apikey, 'si',  latitude, longitude)
    todays_weather.get_forecast()
    current_conditions = todays_weather.current
    for key, value in current_conditions.iteritems():
        print(key   + ': ' + str(value))                        '''

    def get_forecast(self):
        '''Fetches the forecast. Needs to be called after creating object
        Returns False if no forecast can be loaded'''
        if not self.load_forecast():
            return False
        try:
            self.current = self.forecast['currently']
        except:
            pass
        try:
            self.nexthour = self.forecast['minutely']
            self.nexthour_data= self.nexthour['data']
        except:
            pass
        try:
            self.hourly = self.forecast['hourly']
            self.hourly_data = self.hourly['data']
        except:
            pass
        try:
            self.daily = self.forecast['daily']
            self.daily_data = self.daily['data']
        except:
            pass
        try:
            self.alerts = self.forecast['alerts']
        except:
            pass
        try:
            self.flags = self.forecast['flags']
        except:
            pass
        return True

class ForecastTime(Forecast):
    '''Fetches the forecast/weather condtions for the specified latitude
    and longitude for a specific moment in time ranging from approximately
    60 years in the past to 10 years in the future (if the data exists).
    Time is specified as unix time/UTC Epoch Time.'''

    def get_forecast(self):
        '''Fetches the forecast. Needs to be called after creating object'''
        if  not self.load_forecast():
            return False
        

# MAIN

if __name__ == "__main__":
    units = 'si'
    apikey = get_apikey_from_file()
    latitude, longitude = get_latlon_from_file()
    
    #weather = Forecast(apikey, 'si', latitude, longitude)
    #if weather.load_forecast():
    #    for key, value in weather.forecast.iteritems():
    #        print key
    
    #todays_weather = ForecastNow(apikey, units, latitude, longitude)
    #if todays_weather.get_forecast():
    #    current_conditions = todays_weather.current
    #    for key, value in current_conditions.iteritems():
    #        print(key   + ': ' + str(value))
    else:
        print('No Forecast')
