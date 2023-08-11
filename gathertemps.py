#!/usr/bin/python
#-------------------------------------------------------------------gathertemps.py
# pull temperature sensor data from prometheus server
# 
# (C) D Delmar Davis 2023 
#
# Note: POC lots of hard coded foo here....

import requests
import sys
import json

response = requests.get('{0}/api/v1/query'.format('http://bunnyfoofoo:9090'),
        params={'query': 'home_temperature_farenheit'})
results = response.json()['data']['result']
for r in results:
   print("{0}:{1:.1f}F".format(r['metric']['instance'][0].upper(),
                               r['value'][1]),end='')

