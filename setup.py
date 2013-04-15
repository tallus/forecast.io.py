#!/usr/bin/env python

from distutils.core import setup

setup(
        name = 'forecastio',
        version = '0.1',
        description = 'Module for the Forecast.io api (ver 2)',
        author = 'Paul Munday',
        author_email = 'contactme@paulmunday.net',
        url = 'https://github.com/tallus/forecast.io.py',
        license = 'lgpl-3.0.txt',

        packages = ['forecastio',],
        package_data = {'' : ['lgpl-3.0.txt', 'gpl.txt', 'README']},
        include_package_data = True,
        install_requires = [
            'requests>= 0.8.2',
            'pytz>=2011k'
            ],
     )
