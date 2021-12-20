from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json



#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])
model_path = os.path.join(config['output_model_path']) 


#################Function for model scoring
def score_model():
    test_data = pd.DataFrame(
        columns=[
            'corporation',
            'lastmonth_activity',
            'lastyear_activity',
            'number_of_employees',
            'exited']
        )
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
    for file in os.listdir(os.getcwd()+'/'+model_path+'/'):
        counter = 1
        if file.endswith('.pkl'):
            if counter > 1:
                print('There are multiple models in the directory, just one taken')
                break
            model = pickle.load(open(os.getcwd()+'/'+model_path+'/trainedmodel.pkl', 'rb'))
            counter += 1

    
    for file in os.listdir(os.getcwd()+'/'+test_data_path+'/'):
        if file.endswith('.csv'):
            read_data = pd.read_csv(os.getcwd()+'/'+test_data_path+'/'+file)
            test_data = test_data.append(read_data)
        else:
            continue
    y_test = test_data.pop('exited').astype(int)
    X_test = test_data[['lastmonth_activity','lastyear_activity','number_of_employees']]

    predictions = model.predict(X_test)

    scores = metrics.f1_score(y_test, predictions)

    if os.path.isdir(os.getcwd()+'/'+model_path):
        with open(os.getcwd()+'/'+model_path+'/'+'latestscore.txt', 'w') as f:
            f.write(str(scores))
    else:
        os.mkdir(os.getcwd()+'/'+model_path)
        with open(os.getcwd()+'/'+model_path+'/'+'latestscore.txt', 'w') as f:
            f.write(str(scores))
    
if __name__ == '__main__':
    score_model()