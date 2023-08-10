#!/usr/bin/python
import requests
import sys
import json

response = requests.get('{0}/api/v1/query'.format('http://bunnyfoofoo:9090'),
        params={'query': 'home_temperature_farenheit'})
results = response.json()['data']['result']
for r in results:
   #print(r)
   print(r['metric']['instance'][0].upper(),":",r['value'][1]," ",sep='',end='')

