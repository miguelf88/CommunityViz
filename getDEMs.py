# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 09:27:49 2020

@author: mafer
"""
import requests
import json
import timeit
import zipfile
import numpy as np
from IPython.display import clear_output

# create timers
def get_time(timer):
    minutes, seconds = int(np.floor(timer)), round(np.ndarray.item(timer % 1)*60)
    return[minutes,  seconds]

# Set url
url = 'https://viewer.nationalmap.gov/tnmaccess/api/products?datasets=National+Elevation+Dataset+%28NED%29+1%2F9+arc-second&bbox=-81.1139%2C35.3845%2C-78.7408%2C36.6111&q=&dateType=dateCreated&start=&end=&polyCode=&polyType=&offset=&max=&outputFormat=JSON&_csrf=1155e4b6-3d4d-409c-8058-99083bab2c28'

# request data
response = requests.get(url)

print('The API from the National Map returned {} features'.format(response.json()['total']))

# load data
data  = response.json()

# grab download url
download_list = []

for item in data['items']:
    download_list.append(item['downloadURL'])
    
# start a timer
start = timeit.default_timer()

# iterate through download_list
for url in download_list:
 
    clear_output(wait=True)
    print('Requesting {}'.format(url.split(sep='/')[7]))
    
    r = requests.get(url)
    
    clear_output(wait=True)
    print('Successfully requested {}'.format(url.split(sep='/')[7]))
    
    with open('data.zip', 'wb') as f:
        f.write(r.content)
    
    clear_output(wait=True)
    print('Opened {}'.format(url.split(sep='/')[7]))
        
    with zipfile.ZipFile('data.zip', 'r') as data_zip:
        data_zip.extractall()
    
    clear_output(wait=True)
    print('Extracted {}'.format(url.split(sep='/')[7]))

# Clear output from underneath cell
clear_output(wait=True)    
    
# get the current time on timer
stop = timeit.default_timer()
timer = np.array([(stop-start)/60])
min_sec = get_time(timer)
minutes, seconds = min_sec[0], min_sec[1]

print('Data successfully downloaded.\nTotal time:', minutes, 'minutes', seconds, 'seconds')