#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright Paul Munday 2013

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from forecastio import Forecast
from forecastio import get_days, get_timestamp, from_timestamp, printuc, get_apikey_from_file
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


if __name__ == "__main__":
    units = 'uk'
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
        
        heading = [' ', 'Min Temp', 'Max Temp', 'Rain', 'Summary']
        print(' '.join(('%*s' % (10, x) for x in heading)))
    
        days=get_days()
        for i in range(7):
            day = days[i]
            wdata = todays_weather.daily_data[i]
            if 'precipIntensity' in wdata:
                if 'precipProbability' in wdata:
                    precip = str(wdata['precipProbability'] * 100) + '%/' + str(round(wdata['precipIntensity'],2)) +'mm'
                else:
                    precip = str(round(wdata['precipIntensity'],2)) +'mm'
            else:
                precip = '-'
            line = [day_abbr[day], str(wdata['temperatureMin']) + u'\xb0C',
                    str(wdata['temperatureMax']) + u'\xb0C', precip, wdata['summary']]
            print(' '.join(('%*s' % (10, x) for x in line)))
    else:
        print('No Forecast')
