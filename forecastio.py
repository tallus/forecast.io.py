#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Python Module for use with the forecast.io api v2'''


# Copyright Paul Munday 2013

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU  Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.

#    You should have received a copy of the GNU  Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import json
import datetime
from datetime import date
from datetime import datetime
from calendar import timegm
import pytz
from pytz import timezone
from time import mktime

# FUNCTION DEFINITIONS

def get_days():
    '''returns a list of days of the week as  integers, 
    where Monday is 0 and Sunday is 6,
    and days[0] = today e.g. if today is Tuesday days[0] == 1   
    Can be used with calendar.day_name and calendar.day_abbr'''
    today = date.today()
    tnum = today.weekday()
    days = []
    for i in range(7):
        x = tnum + i
        if x < 7:
            days.append(x)
        else:
            days.append(x - 7)
    return days

def get_timestamp(year, month, day, hour = 0 ,minute = 0, second = 0, timezone = None):
    '''Returns the number of seconds since Jan 1 1970. 
    Hour, minute, second are optional.
    Timezone is optional and supplied as a string (not a timezone object).
    Naive local time is assumed if timezone is not supplied. '''
    if timezone:
        tz = timezone(timezone)
        dt = tz.localize(datetime(year, month, day, hour, minute, second))
        return timegm(dt.utctimetuple())
    else:
        dt = datetime(year, month, day, hour, minute, second)
        return int(mktime(dt.timetuple()))

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

def printuc(unicodeobj):
    ''' prints as unicode not ASCII'''
    #print(unicode(unicodeobj))
    print(unicodeobj.encode('utf-8'))

# CLASS DEFINITIONS

class Forecast():
    ''' Base class for forecasts using the forecast.io api
    Creates an object containg the various forecasts for the present 
    moment in time for the specified latitude and longitude if time 
    is not present, otherwise at the specified time.
    
    The class takes the following parameters:
    apikey, units , latitude, longitude, time

    units is one of us,si or uk. us gives Imperial measurements,
    si metric. uk is as si except for wind speed in miles per hour.

    Time is Epoch/unix time i.e. seconds since 1970-01-01 00:00 GMT
    
    You will need to call the get_forecast method in order to fetch the data.
   
    N.B. all strings (both keys and values) are returned unicode encoded.
    This is  an issue with the summary which tends to use  character (u'\xb0')

    The Forecasts are:
    self.forecast           An list containing the entire forecast returned
                            note self.current = self.forecast['currently'], 
                            self.nexthour =self.forecast['minutely']
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
    self.daily_data         Based on aggregates that represent the whole day
    self.alerts             Any severe weather warnings issued. A list of
                            dictionaries contains:
                            title:      short text sumamry
                            expires:    unix time the warning expires
                            uri:        url that contains detailed info
    self.flags              Meta data such as source of data see:
                            https://developer.darkskyapp.com/docs/v2
                            sources = list of sources used, 
                            si  = si units were used if present

    In addition the following should be present

    self.latitude           latitude requested
    self.longtitude         longitude requested
    self.timezone           IANA timezone used for the forecasts. N.B. the 
                            api docs state is is preferable to use local
                            settings if preference to this, where possible
    self.offset             Timezone offset from GMT/UTC

    N.B. Any one data set (current, nexthour, hourly, daily, alerts, flags etc) 
    may or may not be present. In determining a forecast you should check
    to see what if it is available at the most accurate level and fall back
    to the next most accurate if not. In particular it appears that nexthour
    is often  missing or lacking data. Alerts will only be present if there
    are actual alerts. No exceptions will be raised if data is missing.
    
    Forecasts contain  the following

    summary             Human readable summary
    icon                Machine readable version of summary consisting of one of
                        clear-day, clear-night, rain, snow, sleet, wind, fog,
                        cloudy, partly-cloudy-day, or partly-cloudy-night
                        These may change in future. You should set a sensible
                        default if you rely on theses.
    data                (see below)

    The following are  grouped together in the data set,
    as a dictionary/list of dictionaries. e.g. self.current['temperature'] 
    None of them are guaranteed to present.
   
    time                Epoch(unix) time at which the data point occurs
    sunriseTime         Epoch/unix time. Daily only.
    SunsetTime          
    precipIntensity     "A numerical value representing the intensity 
                        (in inches of liquid water per hour) of precipitation 
                        occurring at the given time conditional on probability 
                        (that is, assuming any precipitation occurs at all).
                        A very rough guide is that a value of 0 corresponds 
                        to no  precipitation, 0.002 corresponds to very light
                        sprinkling, 0.017 corresponds to light precipitation,
                        0.1 corresponds to moderate precipitation, and 
                        0.4 corresponds to very heavy precipitation."
                        (as  measured inches per hour ,  or mm/24.5)
                        us: Inches per hour si/uk: Millimeters per hour
    precipProbability   Probability of precipitation expressed as a value 
                        between 0 and 1 (not defined if precipIntenstiy is 0) 
    precipType          String: rain,snow,sleet* or hail  *Also used to describe
                        freezing rain, wintery mix,ice pellets
                        (not defined if precipIntenstiy is 0) 
    precipAccumulation  Daily only. Amount of snowfall expected Only present 
                        when snow is expected
                        us: Inches si/uk: Centimeters
    temperature         us Degrees Fahrenheit si/uk: Degrees Celcius 
                        Not present in daily.
    temperatureMin      Daily only.
    temperatureMax
    temperatureMinTime  Daily only. Epoch time this will occur.
    temperatuteMaxTime
    windSpeed           us/uk: Miles per hour  si: Meters per second
    windBearing         Direction in degrees where true north = 0 degrees
    cloudCover          Precentage of cloud cover as a number between 0 & 1
                        0 = clear sky, 0.4 =  scattered clouds 
                        0.75 =  Broken cloud cover 1 = completely overcast
    humidity            relative humidity  as bumber between 0 & 1
    pressure            us: millibars si/uk:hectopascals (==millibars)
    visibility          average visibilty, capped at 10 miles
                        us:Miles si/uk: Kilometers

    All of the  may, optionally, have an associated Error value defined 
    (with the property precipIntensityError, windSpeedError,pressureError, etc.)
    representing forecast.io's confidence in its prediction. 

    Example:
    ========

    todays_weather = ForecastNow(apikey, 'si',  latitude, longitude)
    todays_weather.get_forecast()
    current_conditions = todays_weather.current
    for key, value in current_conditions.iteritems():
        print(key   + ': ' + str(value))                        '''

    def __init__(self, apikey, units, latitude, longitude, time = None):
        self.apikey = apikey
        self.units = units
        self.lat = latitude
        self.lon = longitude
        self.timestamp = time
        if time:
            self.url = 'https://api.forecast.io/forecast/' + str(apikey) +  '/' + str(latitude) + ',' + str(longitude) + ',' + str(time) + '?units=' + units
        else:
            self.url = 'https://api.forecast.io/forecast/' + str(apikey) +  '/' + str(latitude) + ',' + str(longitude) + "?units=" + units

    def get_forecast(self):
        '''Fetches the forecast. Needs to be called after creating object
        Returns False if no forecast can be loaded'''
        try:
            r = requests.get(self.url)
        except:
            return False
        else:
            self.forecast = json.loads(r.content)

        if 'currently' in self.forecast:
            self.current = self.forecast['currently']
        if 'minutely' in self.forecast:
            self.nexthour = self.forecast['minutely']
            self.nexthour_data= self.nexthour['data']
        if 'hourly' in self.forecast:
            self.hourly = self.forecast['hourly']
            self.hourly_data = self.hourly['data']
        if 'daily' in self.forecast:
            self.daily = self.forecast['daily']
            self.daily_data = self.daily['data']
        if 'alerts' in self.forecast:
            self.alerts = self.forecast['alerts']
        if 'flags' in self.forecast:
            self.flags = self.forecast['flags']
        if 'latitude' in self.forecast:
            self.latitude = self.forecast['latitude'] # see also self.lat 
        else:
            self.latitude = self.lat
        if 'longitude' in self.forecast:
            self.longitude = self.forecast['longitude'] # see also self.lon
        else:
            self.longitude  = self.lon
        if 'time' in self.forecast:
            self.time = self.forecast['time'] # see also self.timestamp
        else:
            self.time = self.timestamp
        if 'timezone' in self.forecast:
            self.timezone = self.forecast['timezone']
        if 'offset' in self.forecast:
            self.offset = self.forecast['offset'] 
        return True


# list of possible datapoints for data sets
datapoints = ['time', 
            'sunriseTime', 
            'sunsetTime', 
            'precipIntensity',
            'precipProbability',
            'precipType',
            'precipAccumulation',
            'temperature',
            'temperatureMin'
            'temperatureMax',
            'temperatureMinTime',
            'temperatureMaxTime',
            'windSpeed',
            'windBearing',
            'cloudCover',
            'humidity',
            'pressure',
            'visibility']


# MAIN

#if __name__ == "__main__":

