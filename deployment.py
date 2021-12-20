from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import shutil
import os
from scipy.sparse import data
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json



##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
prod_deployment_path = os.path.join(config['prod_deployment_path'])
model_path = os.path.join(config['output_model_path'])  


####################function for deployment
def store_model_into_pickle():
    if os.path.isdir(os.getcwd()+'/'+prod_deployment_path) == False:
        os.mkdir(os.getcwd()+'/'+prod_deployment_path)
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    files = [os.getcwd()+'/'+model_path+'/'+file for file in os.listdir(os.getcwd()+'/'+model_path+'/') if file.endswith('.pkl')]
    latest_file = max(files, key=os.path.getctime)
    shutil.copy2(latest_file, os.getcwd()+'/'+prod_deployment_path)

    shutil.copy2(os.getcwd()+'/'+dataset_csv_path+'/'+'ingestedfiles.txt', os.getcwd()+'/'+prod_deployment_path)

    shutil.copy2(os.getcwd()+'/'+model_path+'/'+'latestscore.txt', os.getcwd()+'/'+prod_deployment_path)
        
        
if __name__ == '__main__':
    store_model_into_pickle()
