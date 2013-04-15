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
        long_description = """ forecastio is a python module to access the \
                forecast.io API version 2 (https://developer.darkskyapp.com/)\
                you will need to register for an API key.
                It allows for the creation of objects with easy access to \
                the weather forecast data  the API provides.""",
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)'
            'Natural Language :: English',
            'Programming Language :: Python :: 2.7'
            'Topic :: Scientific/Engineering :: Atmospheric Science'
            'Topic :: Software Development :: Libraries :: Python Modules'
            ],
        packages = ['forecastio',],
        package_data = {'' : ['lgpl-3.0.txt', 'gpl.txt', 'README']},
        include_package_data = True,
        install_requires = [
            'requests>= 0.8.2',
            'pytz>=2011k'
            ],
     )
