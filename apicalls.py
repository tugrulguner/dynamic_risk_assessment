import requests
import os
import pandas as pd
import json
from flask import Flask, session, jsonify, request

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000/"

with open('config.json','r') as f:
    config = json.load(f) 

test_data_path = os.path.join(config['test_data_path']) 
output_model = os.path.join(config['output_model_path']) 

path = json.dumps(os.getcwd()+'/'+test_data_path+'/'+'testdata.csv')
#Call each API endpoint and store the responses
response1 = requests.post(URL+'prediction', data=path).text
response2 = requests.get(URL+'scoring').text
response3 = requests.get(URL+'diagnostics').text
response4 = requests.get(URL+'summarystats').text

#combine all API responses
responses = [
  f'prediction is {response1}', 
  f'Scoring is {response2}', 
  f'Diagnostics is {response3}', 
  f'Summary stats are {response4}'
  ]

#write the responses to your workspace
with open(os.getcwd()+'/'+output_model+'/'+'responses.txt', 'w') as f:
  for el in responses:
    f.write(el+'\n')


