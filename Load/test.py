
import requests
import csv
import pandas as pd
from datetime import datetime
import re
import pandas as pd
import urllib




def get_price_data(query):
    print (query)
    params_string=''
    for key,value in query.items():
        params_string=params_string+'&{}={}'.format(key,value)
    url = "https://www.google.com/finance/getprices?"+params_string[1:]
    print (url)
    with urllib.request.urlopen(url) as response:
        html=response.read
        print(html)
    #print("URL" ,r.url)
    #lines = r.text.splitlines()
    #print(r)

param = {'q': 'INFY',
         'i': '60',
         'x': 'NSE',
         'p': '2d'
         }

get_price_data(param)
